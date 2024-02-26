import base64
import mimetypes
from io import BytesIO

import magic
import os
import pprint
import glob

from flask_restful import Resource, request, abort
from flask import send_from_directory
from werkzeug.utils import secure_filename

from backend.api.common.auth_http_token import auth
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_user, define_schema
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.route import Route
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.config.fields import files_webadmins_fields


class FileDownloadOpenLDAPResource(Resource):
    # @auth.login_required(role=[Role.WEB_ADMIN, Role.SIMPLE_USER])
    # @permission_user()
    def get(self, name, *args, **kwargs):
        return send_from_directory(
            os.path.join(settings.ABSPATH_UPLOAD_FOLDER), name
        )


class FileUploadOpenLDAPResource(Resource, CommonSerializer):

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

        base64_data = user.jpegPhoto
        print(len(base64_data))
        return {}, 200
        route = os.path.join(
            os.path.join(settings.UPLOAD_FOLDER, settings.FOLDER_PHOTOS),
            f'{username_uid}.*'
        )

        response_data = {}

        import mimetypes

        print(mimetypes.guess_extension('image/png'))
        for path in glob(route):
            with open(path, 'rb') as f:
                # base64_encoded = base64.b64encode(f.read())
                byte_data_file = f.read()
                byte_data_base64_dec = base64.b64decode(base64_data)
            if not byte_data_file == byte_data_base64_dec:
                with open('asd') as f:
                    pass
            # if not response_data.get('jpegPhoto'):
            #     response_data['jpegPhoto'] = []
            # response_data['jpegPhoto'].append(path)

        return response_data, 200
        # with open(,'rb') as f:
        #     f.read()

    @auth.login_required(role=[Role.WEB_ADMIN])
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
            if not save_deserialize_data.get(key):
                save_deserialize_data[key] = []

            if not files:
                path = os.path.join(
                    settings.ABSPATH_UPLOAD_FOLDER,
                    f'{username_uid}*.*'
                )
                files = glob.glob(path)
                # must be done

            for index, file in enumerate(files):
                chunks = b''.join(file.stream)
                filename_secure = secure_filename(file.filename)
                saving_filename = f'{username_uid}_{key}_{index}.{filename_secure.rsplit(".", 1)[1].lower()}'

                if not response_data.get(key):
                    response_data[key] = []
                response_data[key].append(os.path.join(
                    '/', settings.UPLOAD_FOLDER, saving_filename
                ))

                path_to_save = os.path.join(settings.ABSPATH_UPLOAD_FOLDER, saving_filename)

                file_data_exists = b''
                if os.path.exists(path_to_save):
                    with open(path_to_save, 'rb') as f_r:
                        file_data_exists = f_r.read()

                if file_data_exists != chunks: # edit
                    with open(path_to_save, 'wb') as f:
                        f.write(chunks)
                        save_deserialize_data[key].append(base64.b64encode(chunks))

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
