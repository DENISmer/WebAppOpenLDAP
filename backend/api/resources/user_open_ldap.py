from flask_restful import Resource, marshal_with, fields
# import backend.api.common.auth_token as at
from backend.api.common.auth_http_token import auth


resource_fields = {
    'dn': fields.String,
    'uidNumber': fields.Integer,
    'gidNumber': fields.Integer,
    'uid': fields.String,
    'sshPublicKey': fields.List(fields.String),
    'st': fields.String,
    'mail': fields.List(fields.String),
    'street': fields.String,
    'cn': fields.String,
    'displayName': fields.String,
    'givenName': fields.String,
    'sn': fields.String,
}


class UserOpenLDAPResource(Resource):

    @auth.login_required
    @marshal_with(resource_fields)
    def get(self, uid, **kwargs):

        return None, 200

    @auth.login_required
    def post(self):
        pass

    @auth.login_required
    def patch(self):
        pass

    @auth.login_required
    def delete(self):
        pass


class UserListOpenLDAPResource(Resource):

    @auth.login_required
    def get(self):
        return {'User': 'UserOpenLDAP'}, 200

    @auth.login_required
    def post(self):
        pass
