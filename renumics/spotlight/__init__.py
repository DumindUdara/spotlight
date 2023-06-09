"""
Renumics Spotlight
"""

from loguru import logger
from .backend.cache import clear_data_cache
from .__version__ import __version__
from .dataset import Dataset
from .dtypes import (
    Audio,
    Category,
    Embedding,
    Image,
    Mesh,
    Sequence1D,
    Video,
    Window,
)
from .viewer import Viewer, close, viewers, show
from .plugin_loader import load_plugins
from .settings import settings
from . import logging

if not settings.verbose:
    logging.disable()

__plugins__ = load_plugins()

__all__ = ["show", "close", "viewers", "Viewer", "clear_data_cache"]
