"""
start flask development server
"""

import asyncio
import re
from pathlib import Path
from typing import Any

from fastapi import Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

import httpx
from httpx import AsyncClient

from renumics.spotlight.backend.exceptions import Problem
from renumics.spotlight.develop.project import get_project_info
from renumics.spotlight.plugin_loader import load_plugins
from renumics.spotlight.reporting import (
    emit_exception_event,
    emit_exit_event,
    emit_startup_event,
)
from renumics.spotlight.settings import settings

from .apis import plugins as plugin_api
from .apis import websocket
from .config import Config
from .middlewares.timing import add_timing_middleware
from .tasks.task_manager import TaskManager
from .types import SpotlightApp
from .websockets import WebsocketManager


def create_app() -> SpotlightApp:
    """
    create app
    """

    app = SpotlightApp()

    app.data_source = None
    app.task_manager = TaskManager()
    app.config = Config()
    app.layout = None
    app.project_root = Path.cwd()
    app.vite_url = None
    app.username = ""

    app.include_router(websocket.router, prefix="/api")
    app.include_router(plugin_api.router, prefix="/api/plugins")

    @app.exception_handler(Exception)
    async def _(_: Request, e: Exception) -> JSONResponse:
        if settings.dev:
            logger.exception(e)
        else:
            logger.info(e)
        emit_exception_event()
        class_name = type(e).__name__
        title = re.sub(r"([a-z])([A-Z])", r"\1 \2", class_name)
        return JSONResponse(
            {"title": title, "detail": str(e), "type": class_name},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(Problem)
    async def _(_: Request, problem: Problem) -> JSONResponse:
        if settings.dev:
            logger.exception(problem)
        else:
            logger.info(problem)
        return JSONResponse(
            {
                "title": problem.title,
                "detail": problem.detail,
                "type": type(problem).__name__,
            },
            status_code=problem.status_code,
        )

    for plugin in load_plugins():
        plugin.activate(app)

    @app.on_event("startup")
    def _() -> None:
        loop = asyncio.get_running_loop()
        app.websocket_manager = WebsocketManager(loop)
        emit_startup_event()

    @app.on_event("shutdown")
    def _() -> None:
        app.task_manager.shutdown()
        emit_exit_event()

    try:
        app.mount(
            "/static",
            StaticFiles(packages=["renumics.spotlight.backend"]),
            name="assets",
        )
    except AssertionError:
        logger.warning("Frontend folder does not exist. No frontend will be served.")

    templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

    async def _reverse_proxy(request: Request) -> Response:
        http_server = AsyncClient(base_url=request.app.vite_url)
        url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))

        # NOTE: URL-encoding is not accepted by vite. Use unencoded path instead.
        # pylint: disable-next=protected-access
        url._uri_reference = url._uri_reference._replace(path=request.url.path)

        body = await request.body()

        rp_req = http_server.build_request(
            request.method,
            url,
            headers=request.headers.raw,
            content=body,
        )

        rp_resp = await http_server.send(rp_req, stream=False)

        return Response(
            content=rp_resp.content,
            status_code=rp_resp.status_code,
            headers=rp_resp.headers,
        )

    app.add_route("/src/{path:path}", _reverse_proxy, ["POST", "GET"])
    app.add_route(
        "/node_modules/.vite/dist/client/{path:path}", _reverse_proxy, ["POST", "GET"]
    )
    app.add_route(
        "/node_modules/.vite/deps/{path:path}", _reverse_proxy, ["POST", "GET"]
    )
    app.add_route("/node_modules/.pnpm/{path:path}", _reverse_proxy, ["POST", "GET"])

    @app.get("/")
    def _(request: Request) -> Any:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "dev": settings.dev,
                "dev_location": get_project_info().type,
                "vite_url": request.app.vite_url,
            },
        )

    if settings.dev:
        logger.info("Running in dev mode")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        add_timing_middleware(app)

    return app
