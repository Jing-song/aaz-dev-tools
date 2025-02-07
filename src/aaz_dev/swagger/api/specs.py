from flask import Blueprint, jsonify, url_for, request
from flask.helpers import send_from_directory
import os

from swagger.controller.specs_manager import SwaggerSpecsManager
from swagger.model.specs import OpenAPIResourceProvider, TypeSpecResourceProvider
from swagger.utils.source import SourceTypeEnum

bp = Blueprint('swagger', __name__, url_prefix='/Swagger/Specs')


@bp.route("/Files/<path:file_path>", methods=("GET",))
def get_file(file_path):
    from utils.config import Config
    if not Config.get_swagger_root():
        return jsonify({"error": "Swagger root not found"}), 404
    return send_from_directory(Config.get_swagger_root(), file_path)


@bp.route("/Stat/<path:path>", methods=("GET",))
def get_path_stat(path):
    from utils.config import Config
    root_dir = Config.get_swagger_root()
    if not root_dir:
        # return 200 status code to avoid print error logs in the client side
        return jsonify({"error": "Swagger root not found"})
    path = os.path.join(root_dir, path)
    if not os.path.exists(path):
        # return 200 status code to avoid print error logs in the client side
        return jsonify({"error": "Path not exist"})
    return jsonify({
        "isDir": os.path.isdir(path),
        "isFile": os.path.isfile(path),
    })


# modules
@bp.route("/<plane>", methods=("GET",))
def get_modules_by(plane):
    specs_manager = SwaggerSpecsManager()
    result = []
    for module in specs_manager.get_modules(plane):
        m = {
            "url": url_for('swagger.get_module', plane=plane, mod_names=module.names),
            "name": module.name,
            "folder": module.folder_path,
        }
        result.append(m)
    return jsonify(result)


@bp.route("/<plane>/<list_path:mod_names>", methods=("GET",))
def get_module(plane, mod_names):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    module = specs_module_manager.module
    result = {
        "url": url_for('swagger.get_module', plane=plane, mod_names=mod_names),
        "name": module.name,
        "folder": module.folder_path,
        "resourceProviders": []
    }
    for rp in specs_module_manager.get_resource_providers():
        if isinstance(rp, OpenAPIResourceProvider):
            result['resourceProviders'].append({
                "url": url_for('swagger.get_openapi_resource_provider', plane=plane, mod_names=mod_names, rp_name=rp.name),
                "name": rp.name,
                "folder": rp.folder_path,
                "type": SourceTypeEnum.OpenAPI,
            })
    return jsonify(result)


# resource providers
@bp.route("/<plane>/<list_path:mod_names>/ResourceProviders", methods=("GET",))
def get_resource_providers_by(plane, mod_names):
    # get query param type in request
    rp_type = request.args.get('type', None)
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    result = []
    for rp in specs_module_manager.get_resource_providers():
        if isinstance(rp, OpenAPIResourceProvider):
            if rp_type and rp_type != 'OpenAPI':
                continue
            result.append({
                "url": url_for('swagger.get_openapi_resource_provider', plane=plane, mod_names=mod_names, rp_name=rp.name),
                "name": rp.name,
                "folder": rp.folder_path,
                "type": SourceTypeEnum.OpenAPI
            })
        elif isinstance(rp, TypeSpecResourceProvider):
            if rp_type and rp_type != 'TypeSpec':
                continue
            result.append({
                "url": url_for('swagger.get_typespec_resource_provider', plane=plane, mod_names=mod_names, rp_name=rp.name),
                "name": rp.name,
                "entryFiles": rp.entry_files,
                "type": SourceTypeEnum.TypeSpec,
            })
    return jsonify(result)


# TODO: may need to add OpenAPI segment in the url
@bp.route("/<plane>/<list_path:mod_names>/ResourceProviders/<rp_name>", methods=("GET",))
def get_openapi_resource_provider(plane, mod_names, rp_name):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    rp = specs_module_manager.get_openapi_resource_provider(rp_name)
    result = {
        "url": url_for('swagger.get_openapi_resource_provider', plane=plane, mod_names=mod_names, rp_name=rp.name),
        "name": rp.name,
        "folder": rp.folder_path,
        "type": SourceTypeEnum.OpenAPI,
        "resources": []
    }
    resource_op_group_map = specs_module_manager.get_grouped_resource_map(rp_name)
    for op_group_name, resource_map in resource_op_group_map.items():
        for resource_id, version_map in resource_map.items():
            rs = {
                "opGroup": op_group_name,
                "url": url_for('swagger.get_resource_in_rp',
                               plane=plane, mod_names=mod_names, rp_name=rp.name, resource_id=resource_id),
                "id": resource_id,
                "versions": []
            }
            for version, resource in version_map.items():
                rs['versions'].append({
                    "url": url_for('swagger.get_resource_version_in_rp',
                                   plane=plane, mod_names=mod_names, rp_name=rp.name,
                                   resource_id=resource.id, version=resource.version),
                    "version": version,
                    "file": resource.file_path,
                    "path": resource.path,
                    "operations": resource.operations
                })
            result['resources'].append(rs)
    return jsonify(result)


@bp.route("/<plane>/<list_path:mod_names>/ResourceProviders/<rp_name>/TypeSpec", methods=("GET",))
def get_typespec_resource_provider(plane, mod_names, rp_name):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    rp = specs_module_manager.get_typespec_resource_provider(rp_name)
    result = {
        "url": url_for('swagger.get_typespec_resource_provider', plane=plane, mod_names=mod_names, rp_name=rp.name),
        "name": rp.name,
        "entryFiles": rp.entry_files,
        "type": "TypeSpec",
    }
    return jsonify(result)


# resources
@bp.route("/<plane>/<list_path:mod_names>/ResourceProviders/<rp_name>/Resources", methods=("GET",))
def get_resources_by(plane, mod_names, rp_name):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    result = []
    rp = specs_module_manager.get_openapi_resource_provider(rp_name)
    resource_op_group_map = specs_module_manager.get_grouped_resource_map(rp_name)
    for op_group_name, resource_map in resource_op_group_map.items():
        for resource_id, version_map in resource_map.items():
            rs = {
                "opGroup": op_group_name,
                "url": url_for('swagger.get_resource_in_rp',
                               plane=plane, mod_names=mod_names, rp_name=rp.name, resource_id=resource_id),
                "id": resource_id,
                "versions": []
            }
            for version, resource in version_map.items():
                rs['versions'].append({
                    "url": url_for('swagger.get_resource_version_in_rp',
                                   plane=plane, mod_names=mod_names, rp_name=rp.name,
                                   resource_id=resource.id, version=resource.version),
                    "id": resource_id,
                    "version": version,
                    "file": resource.file_path,
                    "path": resource.path,
                    "operations": resource.operations
                })
            result.append(rs)
    return jsonify(result)


# resource
@bp.route("/<plane>/<list_path:mod_names>/ResourceProviders/<rp_name>/Resources/<base64:resource_id>",
          methods=("GET",))
def get_resource_in_rp(plane, mod_names, rp_name, resource_id):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    version_map = specs_module_manager.get_resource_version_map(resource_id, rp_name)
    rp = list(version_map.values())[0].resource_provider
    op_group_name = specs_module_manager.get_resource_op_group_name(version_map)
    result = {
        "opGroup": op_group_name,
        "url": url_for('swagger.get_resource_in_rp',
                       plane=plane, mod_names=mod_names, rp_name=rp.name, resource_id=resource_id),
        "id": resource_id,
        "versions": []
    }
    for version, resource in version_map.items():
        result['versions'].append({
            "url": url_for('swagger.get_resource_version_in_rp',
                           plane=plane, mod_names=mod_names, rp_name=rp.name,
                           resource_id=resource.id, version=resource.version),
            "id": resource_id,
            "version": version,
            "file": resource.file_path,
            "path": resource.path,
            "operations": resource.operations
        })
    return jsonify(result)


@bp.route("/<plane>/<list_path:mod_names>/Resources/<base64:resource_id>", methods=("GET",))
def get_resource_in_module(plane, mod_names, resource_id):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    version_map = specs_module_manager.get_resource_version_map(resource_id)
    rp = list(version_map.values())[0].resource_provider
    op_group_name = specs_module_manager.get_resource_op_group_name(version_map)
    result = {
        "opGroup": op_group_name,
        "url": url_for('swagger.get_resource_in_rp',
                       plane=plane, mod_names=mod_names, rp_name=rp.name, resource_id=resource_id),
        "id": resource_id,
        "versions": []
    }
    for version, resource in version_map.items():
        result['versions'].append({
            "url": url_for('swagger.get_resource_version_in_rp',
                           plane=plane, mod_names=mod_names, rp_name=rp.name,
                           resource_id=resource.id, version=resource.version),
            "id": resource_id,
            "version": version,
            "file": resource.file_path,
            "path": resource.path,
            "operations": resource.operations
        })
    return jsonify(result)


# resource version
@bp.route(
    "/<plane>/<list_path:mod_names>/ResourceProviders/<rp_name>/Resources/<base64:resource_id>/V/<base64:version>",
    methods=("GET",)
)
def get_resource_version_in_rp(plane, mod_names, rp_name, resource_id, version):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    resource = specs_module_manager.get_resource_in_version(rp_name, resource_id, version)
    result = {
        "url": url_for('swagger.get_resource_version_in_rp',
                       plane=plane, mod_names=mod_names, rp_name=resource.rp_name,
                       resource_id=resource.id, version=resource.version),
        "id": resource_id,
        "version": version,
        "file": resource.file_path,
        "path": resource.path,
        "operations": resource.operations
    }
    return jsonify(result)


@bp.route("/<plane>/<list_path:mod_names>/Resources/<base64:resource_id>/V/<base64:version>", methods=("GET",))
def get_resource_version_in_module(plane, mod_names, resource_id, version):
    specs_module_manager = SwaggerSpecsManager().get_module_manager(plane, mod_names)
    resource = specs_module_manager.get_resource_in_version(resource_id, version)
    result = {
        "url": url_for('swagger.get_resource_version_in_rp',
                       plane=plane, mod_names=mod_names, rp_name=resource.rp_name,
                       resource_id=resource.id, version=resource.version),
        "id": resource_id,
        "version": version,
        "file": resource.file_path,
        "path": resource.path,
        "operations": resource.operations
    }
    return jsonify(result)
