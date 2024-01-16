import pprint

from flask_restful import Resource, marshal_with, fields, reqparse, abort
from backend.api.common.auth_http_token import auth
from backend.api.common.ldap_manager import ConnectionLDAP
from backend.api.common.user_manager import User
from backend.api.config.fields import simple_user_fields, admin_fields


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


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn_ldap = ConnectionLDAP(User(username_uid='bob', userPassword='bob')) # {SSHA}icitv+lYDTUmP2Hsu8eY7MKBrwW8RePP
        self._conn_ldap.connect()

    @auth.login_required
    @marshal_with(resource_fields)
    def get(self, username_uid, *args, **kwargs):
        user = self._conn_ldap.get_user(username_uid)
        return user, 200

    @auth.login_required
    @marshal_with(resource_fields)
    def put(self, username_uid, *args, **kwargs):
        args = parser_put.parse_args()
        pprint.pprint(args)
        return 200

    @auth.login_required
    @marshal_with(resource_fields)
    def patch(self, username_uid):
        args = parser_patch.parse_args()
        user = User(username_uid=username_uid, **args)

        # self._conn_ldap.modify_user(user)
        # user = self._conn_ldap.modify_user(User(username_uid=username_uid, **args))
        return None, 200

    @auth.login_required
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

    @auth.login_required
    @marshal_with(resource_fields_list)
    def get(self):
        return None, 200

    @auth.login_required
    def post(self):
        args = parser_post.parse_args()
        pprint.pprint(args)
        # self._conn_ldap.create_user(User(**args))
        return None, 201
