import pprint

from flask_restful import Resource, marshal_with, fields, reqparse, abort, request
from backend.api.common.auth_http_token import auth
from backend.api.common.decorators import connection_ldap, permission_user
from backend.api.common.ldap_manager import UserManagerLDAP
from backend.api.common.user_manager import User
from backend.api.config.fields import simple_user_fields, admin_fields
from backend.api.common.roles import Role


resource_fields = {
    'dn': fields.String,
    'uidNumber': fields.Integer,
    'gidNumber': fields.Integer,
    'uid': fields.List(fields.String),
    'sshPublicKey': fields.List(fields.String),
    'st': fields.List(fields.String),
    'mail': fields.List(fields.String),
    'street': fields.List(fields.String),
    'cn': fields.List(fields.String),
    'displayName': fields.List(fields.String),
    'givenName': fields.List(fields.String),
    'sn': fields.List(fields.String),
    'postalCode': fields.List(fields.Integer),
}
resource_fields_list = {
    'list': fields.List(
        fields.Nested(resource_fields)
    )
}

parser_post = reqparse.RequestParser()
parser_put = reqparse.RequestParser()
parser_patch = reqparse.RequestParser()
for key, value in admin_fields['fields'].items():
    parser_post.add_argument(
        key, type=value['element_type'], required=True,
        action='append' if value['type'] else None
    )
    parser_put.add_argument(
        key, type=value['element_type'],
        required=True if 'update' in value['operation'] else False,
        action='append' if value['type'] else 'store'
    )
    parser_patch.add_argument(
        key, type=value['element_type'],
        action='append' if value['type'] else 'store'
    )


@auth.get_user_roles  # roles
def get_user_roles(user):
    if user[Role.ADMIN.value]:
        return Role.ADMIN
    return Role.SIMPLE_USER


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_manager_ldap: UserManagerLDAP = None

    @auth.login_required(role=[Role.ADMIN, Role.SIMPLE_USER])
    @marshal_with(resource_fields)
    @connection_ldap
    @permission_user
    def get(self, username_uid, *args, **kwargs):
        self._user_manager_ldap.show_connections()
        print('id conn -', id(self._user_manager_ldap.get_connection()))
        print('id GET', id(self))
        user = self._user_manager_ldap.get_user(username_uid)
        self._user_manager_ldap.is_webadmin(user.dn)

        return user, 200

    @auth.login_required(role=[Role.ADMIN, Role.SIMPLE_USER])
    @marshal_with(resource_fields)
    def put(self, username_uid, *args, **kwargs):
        pprint.pprint(parser_put.args)
        args = parser_put.parse_args()
        pprint.pprint(args)
        return 200

    @auth.login_required(role=[Role.ADMIN, Role.SIMPLE_USER])
    @marshal_with(resource_fields)
    @connection_ldap
    def patch(self, username_uid):
        args = parser_patch.parse_args()
        user = User(username_uid=username_uid, **args)
        self._user_manager_ldap.close_connection()

        self._user_manager_ldap.modify_user(
            user=user,
            fields=admin_fields['fields'],
            operation='update'
        )

        return None, 200

    @auth.login_required(role=[Role.ADMIN])
    def delete(self, username_uid):
        print('DELETE', username_uid)
        # result = self._conn_ldap.delete_user(User(username_uid=username_uid))
        # if not result:
        #     abort(400)

        return 204


class UserListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._user_manager_ldap: UserManagerLDAP = None

    @auth.login_required(role=[Role.ADMIN, Role.SIMPLE_USER])
    @marshal_with(resource_fields_list)
    @connection_ldap
    def get(self):
        print('Current user GET', auth.current_user())
        return None, 200

    @auth.login_required(role=[Role.ADMIN])
    def post(self):
        args = parser_post.parse_args()
        user = User(**args)
        self._user_manager_ldap.create_user(
            user=user,
            fields=admin_fields['fields'],
            operation='create'
        )
        return None, 201
