/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 *
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * a single table column
 * @export
 * @interface Column
 */
export interface Column {
    /**
     *
     * @type {string}
     * @memberof Column
     */
    name: string;
    /**
     *
     * @type {number}
     * @memberof Column
     */
    index?: number;
    /**
     *
     * @type {boolean}
     * @memberof Column
     */
    hidden: boolean;
    /**
     *
     * @type {boolean}
     * @memberof Column
     */
    editable: boolean;
    /**
     *
     * @type {boolean}
     * @memberof Column
     */
    optional: boolean;
    /**
     *
     * @type {string}
     * @memberof Column
     */
    role: string;
    /**
     *
     * @type {Array<any>}
     * @memberof Column
     */
    values: Array<any>;
    /**
     *
     * @type {Array<boolean>}
     * @memberof Column
     */
    references?: Array<boolean>;
    /**
     *
     * @type {string}
     * @memberof Column
     */
    yLabel?: string;
    /**
     *
     * @type {string}
     * @memberof Column
     */
    xLabel?: string;
    /**
     *
     * @type {string}
     * @memberof Column
     */
    description?: string;
    /**
     *
     * @type {Array<string>}
     * @memberof Column
     */
    tags?: Array<string>;
    /**
     *
     * @type {{ [key: string]: number; }}
     * @memberof Column
     */
    categories?: { [key: string]: number };
    /**
     *
     * @type {number}
     * @memberof Column
     */
    embeddingLength?: number;
}

/**
 * Check if a given object implements the Column interface.
 */
export function instanceOfColumn(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && 'name' in value;
    isInstance = isInstance && 'hidden' in value;
    isInstance = isInstance && 'editable' in value;
    isInstance = isInstance && 'optional' in value;
    isInstance = isInstance && 'role' in value;
    isInstance = isInstance && 'values' in value;

    return isInstance;
}

export function ColumnFromJSON(json: any): Column {
    return ColumnFromJSONTyped(json, false);
}

export function ColumnFromJSONTyped(json: any, ignoreDiscriminator: boolean): Column {
    if (json === undefined || json === null) {
        return json;
    }
    return {
        name: json['name'],
        index: !exists(json, 'index') ? undefined : json['index'],
        hidden: json['hidden'],
        editable: json['editable'],
        optional: json['optional'],
        role: json['role'],
        values: json['values'],
        references: !exists(json, 'references') ? undefined : json['references'],
        yLabel: !exists(json, 'y_label') ? undefined : json['y_label'],
        xLabel: !exists(json, 'x_label') ? undefined : json['x_label'],
        description: !exists(json, 'description') ? undefined : json['description'],
        tags: !exists(json, 'tags') ? undefined : json['tags'],
        categories: !exists(json, 'categories') ? undefined : json['categories'],
        embeddingLength: !exists(json, 'embedding_length')
            ? undefined
            : json['embedding_length'],
    };
}

export function ColumnToJSON(value?: Column | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        name: value.name,
        index: value.index,
        hidden: value.hidden,
        editable: value.editable,
        optional: value.optional,
        role: value.role,
        values: value.values,
        references: value.references,
        y_label: value.yLabel,
        x_label: value.xLabel,
        description: value.description,
        tags: value.tags,
        categories: value.categories,
        embedding_length: value.embeddingLength,
    };
}