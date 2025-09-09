from flask_restful_swagger_2 import Resource, swagger
from flask_ldap3_login import AuthenticationResponseStatus
from flask_restful import request, abort
from ldap3 import EXTERNAL

from api.managers.group_ldap_manager_mixin import GroupLDAPManagerMixin
from api.resourses.swagger_schemas import AuthSchemaSwagger
from api.managers.user_ldap_manager import UserFormatDN
from api.managers.ldap_manager import ldap_manager
from api.common.token_manager import TokenManagerDB
from api.common.crypt_passwd import CryptPasswd
from api.common.user_token import UserToken
from api.common.decorators import error_operation_ldap
from api.resourses.schema import AuthLDAPSchema
from api.common.roles import Role
from api.conf import settings


class AuthOpenLDAPResource(Resource):

    @swagger.doc({
        "tags": ["AuthOpenLDAP"],
        "summary": "Create access token",
        "parameters": [
            {
                "in": "body",
                "name": "body",
                "description": "Requested data.",
                "schema": AuthSchemaSwagger,
            },
        ],
        "responses": {
            "200": {
                "description": "Return authenticate information",
                "examples": {
                    "application/json": {
                        'token': "token", 'uid': "user.uid", 'role': "simpleuser"
                    }
                }
            }
        },
    })
    @error_operation_ldap
    def post(self):
        json_data = request.get_json()

        deserialized_data = AuthLDAPSchema().load(json_data)

        user_dn = UserFormatDN().format_dn(identifier=deserialized_data["username"])
        connection = ldap_manager.make_connection(
            bind_user=user_dn,
            bind_password=deserialized_data["userPassword"],
            sasl_mechanism=EXTERNAL
        )
        connection.bind()

        webadmins_group = GroupLDAPManagerMixin(connection).retrieve(Role.WEB_ADMINS.value, attributes=["member"])

        if user_dn in webadmins_group["attributes"]["member"]:
            role = Role.WEB_ADMINS.value
        else:
            role = Role.SIMPLE_USER.value

        crypt_user_password = CryptPasswd(
            password=deserialized_data['userPassword'].encode(),
            secret_key=bytes(settings.SECRET_KEY.encode())
        ).crypt()

        user = UserToken(
            uid=deserialized_data["username"],
            dn=user_dn,
            role=role,
            userPassword=crypt_user_password
        )
        token = TokenManagerDB(user).create_token()
        connection.unbind()

        return {
            'token': token,
            'uid': user.uid,
            'role': user.role
        }


