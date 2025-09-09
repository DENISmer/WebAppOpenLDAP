import os

from flask_restful_swagger_2 import Resource, swagger
from flask_restful import abort, request
from flask import send_from_directory

from api.common.decorators import connection_ldap, error_operation_ldap
from api.managers.file_user_ldap_manager_mixin import FileUserLDAPManagerMixin
from api.common.auth_http_token import auth
from api.common.roles import Role
from api.conf import settings


class FileUploadsOpenLDAPResource(Resource):

    # @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    def get(self, name, *args, **kwargs):
        return send_from_directory(
            os.path.join(settings.ABSPATH_UPLOAD_FOLDER), name
        )


class FileOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["FileUserOpenLDAP"],
        "summary": "Retrieve user's link for jpeg photo",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that get user data",
                "in": "path",
                "type": "string",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "Return changes user's personal information ",
                "examples": {
                    "application/json": {
                        "url": [
                            "/api/v1/files/uploads/margo.png"
                        ]
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def get(self, uid, *args, **kwargs):
        file_manager = FileUserLDAPManagerMixin(self.connection)
        user = file_manager.retrieve(uid, attributes=["jpegPhoto"], is_not_json=True)

        if not user.jpegPhoto.value:
            abort(404, message="Entry not found", status=404)

        global_path = file_manager.save_image(uid, user.jpegPhoto.value)

        return {"url": [global_path]}, 200

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["FileUserOpenLDAP"],
        "summary": "Change user's jpeg photo",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that change user data",
                "in": "path",
                "type": "string",
                "required": True
            },
            {
                "in": "formData",
                "name": "jpegPhoto",
                "type": "file",
                "description": "The file to upload"
            },
        ],
        "responses": {
            "200": {
                "description": "Return changes user's personal information",
                "examples": {
                    "application/json": {
                        "url": [
                            "/api/v1/files/uploads/margo.png"
                        ]
                    }
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def patch(self, uid, *args, **kwargs):
        file_manager = FileUserLDAPManagerMixin(self.connection)
        files_b64 = []

        global_path = []
        for key, file in request.files.items():

            if key != "jpegPhoto":
                abort(400, message="Invalid attribute", status=400)

            file_bytes = b''.join(file.stream)

            _, extension = file_manager.mimetypes(file_bytes)
            if extension[1:] not in settings.ALLOWED_EXTENSIONS:
                abort(400, message="Invalid input file", status=400)

            global_path.append(file_manager.save_image(uid, file_bytes))
            files_b64.append(file_bytes)

        file_manager.modify(uid, changes={
            "jpegPhoto": files_b64
        })

        return {"url": global_path}, 200

    @auth.login_required(role=[Role.WEB_ADMINS, Role.SIMPLE_USER])
    @swagger.doc({
        "tags": ["FileUserOpenLDAP"],
        "summary": "Delete jpeg photo user's",
        "parameters": [
            {
                "name": "uid",
                "description": "unique identifier that delete user data",
                "in": "path",
                "type": "string",
                "required": True
            },
        ],
        "responses": {
            "204": {
                "description": "Return null",
                "examples": {
                    "application/json": {}
                }
            }
        },
        "security": [
            {"api_key": []}
        ]
    })
    @error_operation_ldap
    @connection_ldap
    def delete(self, uid, *args, **kwargs):
        file_manager = FileUserLDAPManagerMixin(self.connection)

        file_manager.modify(uid, changes={
            "jpegPhoto": []
        })
        return None, 204
