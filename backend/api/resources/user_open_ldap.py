from flask_restful import Resource, marshal_with, fields, reqparse
from typing import List, AnyStr
from backend.api.common.auth_http_token import auth
from backend.api.common.ldap_manager import ConnectionLDAP
from backend.api.common.user_manager import User

resource_fields = {
    'dn': fields.String,
    'uidNumber': fields.List(fields.String),
    'gidNumber': fields.List(fields.String),
    'uid': fields.List(fields.String),
    'sshPublicKey': fields.List(fields.String),
    'st': fields.List(fields.String),
    'mail': fields.List(fields.String),
    'street': fields.List(fields.String),
    'cn': fields.List(fields.String),
    'displayName': fields.List(fields.String),
    'givenName': fields.List(fields.String),
    'sn': fields.List(fields.String),
}

parser = reqparse.RequestParser()
parser.add_argument('uid', type=str, required=True, action='append')  # list of string
parser.add_argument('gidNumber', type=int, required=True, action='append')  # list of string
parser.add_argument('givenName', type=str, required=True, action='append')  # list of string
parser.add_argument('dn', type=str, required=True)


class UserOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn_ldap = ConnectionLDAP(User(uid='bob', userPassword='bob')) # {SSHA}icitv+lYDTUmP2Hsu8eY7MKBrwW8RePP
        self._conn_ldap.connect()

    @auth.login_required
    @marshal_with(resource_fields)
    def get(self, uid, *args, **kwargs):
        data = self._conn_ldap.get_user(uid)
        return User(**data['attributes'], dn=data['dn']), 200

    @auth.login_required
    @marshal_with(resource_fields)
    def put(self, uid, *args, **kwargs):
        return 200

    @auth.login_required
    @marshal_with(resource_fields)
    def patch(self, uid):
        user = self._conn_ldap.modify_user(User(uid=uid))
        return {'dn': user.dn}, 200

    @auth.login_required
    def delete(self):
        return 204


class UserListOpenLDAPResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn_ldap = ConnectionLDAP(User(uid='bob', userPassword='bob'))
        self._conn_ldap.connect()

    @auth.login_required
    def get(self):
        return {'User': 'UserOpenLDAP'}, 200

    @auth.login_required
    def post(self):
        args = parser.parse_args()
        self._conn_ldap.create_user(User(**args))
        return 201
