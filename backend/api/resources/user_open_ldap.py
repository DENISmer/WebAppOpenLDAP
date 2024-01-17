import pprint

from flask_restful import Resource, marshal_with, fields, reqparse, abort, request
from backend.api.common.auth_http_token import auth
from backend.api.common.decorators import connection_ldap
from backend.api.common.ldap_manager import ConnectionLDAP
from backend.api.common.user_manager import User
from backend.api.config.fields import simple_user_fields, admin_fields
from backend.api.common.roles import Roles

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
    if user['admin']:
        return Roles.ADMIN
    return Roles.SIMPLE_USER


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dn='uid=bob,ou=People,dc=example,dc=com', userPassword='bob')
        self._conn_ldap = ConnectionLDAP(User())  # {SSHA}icitv+lYDTUmP2Hsu8eY7MKBrwW8RePP
        self._conn_ldap.connect()

    @auth.login_required(role=[Roles.ADMIN, Roles.SIMPLE_USER])
    @marshal_with(resource_fields)
    @connection_ldap
    def get(self, username_uid, *args, **kwargs):
        user = self._conn_ldap.get_user(username_uid)
        self._conn_ldap.is_webadmin()
        print('connection -', kwargs['connection'])
        print('-X GET id: %d, id conn: %d' % (id(self._conn_ldap), id(self._conn_ldap.get_connection())))
        # print('current_user:', auth.current_user())
        return user, 200

    @auth.login_required(role=[Roles.ADMIN, Roles.SIMPLE_USER])
    @marshal_with(resource_fields)
    def put(self, username_uid, *args, **kwargs):
        args = parser_put.parse_args()
        pprint.pprint(args)
        return 200

    @auth.login_required(role=[Roles.ADMIN, Roles.SIMPLE_USER])
    @marshal_with(resource_fields)
    def patch(self, username_uid):
        args = parser_patch.parse_args()
        user = User(username_uid=username_uid, **args)

        self._conn_ldap.modify_user(
            user=user,
            fields=admin_fields['fields'],
            operation='update'
        )

        return None, 200

    @auth.login_required(role=[Roles.ADMIN])
    def delete(self, username_uid):
        print('DELETE', username_uid)
        # result = self._conn_ldap.delete_user(User(username_uid=username_uid))
        # if not result:
        #     abort(400)

        return 204


class UserListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._conn_ldap = ConnectionLDAP(User(username_uid='bob', userPassword='bob'))
        self._conn_ldap.connect()

    @auth.login_required(role=[Roles.ADMIN, Roles.SIMPLE_USER])
    @marshal_with(resource_fields_list)
    def get(self):
        print('Current user GET', auth.current_user())
        return None, 200

    @auth.login_required(role=[Roles.ADMIN])
    def post(self):
        args = parser_post.parse_args()
        user = User(**args)
        self._conn_ldap.create_user(
            user=user,
            fields=admin_fields['fields'],
            operation='create'
        )
        return None, 201
