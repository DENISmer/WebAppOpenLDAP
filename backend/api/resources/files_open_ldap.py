import base64
import os
import pprint

from flask_restful import Resource, request, abort

from werkzeug.utils import secure_filename

from backend.api.common.auth_http_token import auth
from backend.api.common.common_serialize_open_ldap import CommonSerializer
from backend.api.common.decorators import connection_ldap, permission_user, define_schema
from backend.api.common.managers_ldap.user_ldap_manager import UserManagerLDAP
from backend.api.common.roles import Role
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.config.fields import files_webadmins_fields


class FileOpenLDAPResource(Resource, CommonSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

    @auth.login_required(role=[Role.WEBADMIN])
    @connection_ldap
    @permission_user()
    @define_schema
    def patch(self, file_username_uid, *args, **kwargs):

        files_schema = 'FilesSchema' #kwargs['schema']
        files_fields = files_webadmins_fields #kwargs['fields']

        user = UserManagerLDAP(connection=self.connection).item(username_uid)
        if not user:
            abort(404, message='User not found', status=404)

        # print('files', request.files)
        # print('files', request.files.to_dict())
        # # pprint.pprint(request.__dict__)
        # deserialize_data = self.deserialize_data(files_schema, request.files.to_dict(), partial=True)
        # print('OUT')
        # pprint.pprint(deserialize_data)
        # data = deserialize_data['jpegPhoto'].stream
        # # base64_data = b''
        # byte_data = b''
        # for item in data:
        #     # base64_data += base64.b64encode(item)
        #     byte_data += item
        # # print('len', len(base64_data))
        # print('OUT')
        # base64_data = base64.b64encode(byte_data)
        # with open(os.path.join(settings.UPLOAD_FOLDER, 'file1.png'), 'wb') as f:
        #     base64_decode = base64.b64decode(base64_data)
        #     print(base64_decode == byte_data)
        #     f.write(base64_decode)
        #
        # file = deserialize_data['jpegPhoto']
        # filename = secure_filename(file.filename)
        # with open(os.path.join(settings.UPLOAD_FOLDER, f'{username_uid}.{filename.rsplit(".", 1)[1].lower()}'), 'wb') as f1:
        #     f1.write(byte_data)
        #
        # print('filename', filename)
        # file.save(os.path.join(
        #     settings.UPLOAD_FOLDER, filename #f'{username_uid}.{filename.rsplit(".", 1)[1].lower()}'
        # ))
        #
        # abort(400, message='exit', status=400)

        deserialize_data = self.deserialize_data(files_schema, request.files.to_dict(), partial=True)

        for key, value in deserialize_data.items():
            chunks = b''.join(value.stream)
            file = value
            filename = secure_filename(file.filename)
            with open(
                    os.path.join(
                        os.path.join(settings.UPLOAD_FOLDER, settings.FOLDER_PHOTOS),
                        f'{username_uid}.{filename.rsplit(".", 1)[1].lower()}'
                    ),
            'wb') as f:
                f.write(chunks)
                base64_chunks = base64.b64encode(chunks)
                deserialize_data[key] = base64_chunks

        updated_user = UserLdap(
            dn=user.dn,
            username=username_uid,
            fields=files_fields['fields'],
            input_field_keys=deserialize_data.keys(),
            **deserialize_data,
        )
        user_obj = UserManagerLDAP(connection=self.connection)

        user_obj.modify(
            item=updated_user,
            operation='update',  # deprecate
            not_modify_item=user
        )
