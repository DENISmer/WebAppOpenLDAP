import base64
import mimetypes
from io import BytesIO

import magic
import os
import pprint
import glob

import orjson
from flask_restful import Resource, request, abort
from flask import send_from_directory
from werkzeug.utils import secure_filename

from backend.api.common.auth_http_token import auth
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_user, define_schema
from backend.api.common.file_rewritter import rewrite_file, del_files
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.route import Route
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.config.fields import files_webadmins_fields


class FileUploadsOpenLDAPResource(Resource):
    # @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    # @permission_user()
    def get(self, name, *args, **kwargs):
        return send_from_directory(
            os.path.join(settings.ABSPATH_UPLOAD_FOLDER), name
        )


class FileOpenLDAPResource(Resource, CommonSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None
        self.route = Route.FILES

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def get(self, username_uid, *args, **kwargs):
        user = UserManagerLDAP(connection=self.connection) \
            .item(username_uid, ['jpegPhoto'])
        if not user:
            abort(404, message='User not found', status=404)

        response = rewrite_file(user, files_webadmins_fields['fields'])
        user.__dict__.update(response)

        return response, 200

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    @define_schema
    def patch(self, username_uid, *args, **kwargs):
        files_schema = kwargs['schema']
        files_fields = kwargs['fields']

        user = UserManagerLDAP(connection=self.connection).item(username_uid)
        if not user:
            abort(404, message='User not found', status=404)

        deserialize_data = self.deserialize_data(files_schema, request.files, partial=True)

        response_data = {}
        save_deserialize_data = {}
        for key, files in deserialize_data.items():

            for index, file in enumerate(files):
                chunks = b''.join(file.stream)

                if not response_data.get(key):
                    response_data[key] = []

                format_file = magic.from_buffer(chunks, mime=True)
                print('FILESOPENLDAP')
                print('format_file', format_file)
                extension_tmp = mimetypes.guess_extension(format_file) if not format_file == 'image/webp' else '.webp'
                if not extension_tmp:
                    abort(
                        400,
                        fields={key: {"0": ['File is not allowed']}},
                        status=400
                    )

                print('extension', extension_tmp)
                print('file.filename', file.filename)

                extension = file.filename.rsplit('.', 1)[1].lower()
                saving_filename = f'{username_uid}_{key}_{index}{extension_tmp}' # .{extension}
                print('saving_filename', saving_filename)
                print('FILESOPENLDAP')
                response_data[key].append(os.path.join(
                    settings.GLOBAL_UPLOAD_FOLDER, saving_filename
                ))
                path_to_save = os.path.join(settings.ABSPATH_UPLOAD_FOLDER, saving_filename)
                tmp_filename = f'{username_uid}_{key}_{index}*'

                del_files(path_to_save=path_to_save, filename=tmp_filename)

                file_data_exists = b''
                if os.path.exists(path_to_save):
                    with open(path_to_save, 'rb') as f_r:
                        file_data_exists = f_r.read()

                data_chunks = chunks

                if file_data_exists != data_chunks: # edit
                    if not save_deserialize_data.get(key):
                        save_deserialize_data[key] = []
                    with open(path_to_save, 'wb') as f:
                        f.write(chunks)
                        save_deserialize_data[key].append(
                            data_chunks
                        )

        if save_deserialize_data:
            updated_user = UserLdap(
                dn=user.dn,
                username=username_uid,
                fields=files_fields['fields'],
                input_field_keys=save_deserialize_data.keys(),
                **save_deserialize_data,
            )
            user_obj = UserManagerLDAP(connection=self.connection)

            user_obj.modify(
                item=updated_user,
                operation='update',  # deprecate
                not_modify_item=user
            )

        return response_data, 200

    @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    @connection_ldap
    @permission_user()
    def delete(self, username_uid, *args, **kwargs):
        user = UserManagerLDAP(connection=self.connection).item(username_uid)
        if not user:
            abort(404, message='User not found', status=404)

        updated_user = UserLdap(
            dn=user.dn,
            username=username_uid,
            fields=files_webadmins_fields['fields'],
            input_field_keys=['jpegPhoto'],
            **{'jpegPhoto': []},
        )
        user_obj = UserManagerLDAP(connection=self.connection)

        user_obj.modify(
            item=updated_user,
            operation='update',  # deprecate
            not_modify_item=user
        )

        tmp_filename = f'{username_uid}_jpegPhoto_*'
        del_files(filename=tmp_filename)

        return None, 204
