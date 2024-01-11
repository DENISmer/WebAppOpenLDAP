from flask_restful import Resource
# import backend.api.common.auth_token as at
from backend.api.common.auth_http_token import auth


class UserOpenLDAPResource(Resource):

    @auth.login_required
    def get(self, uid):
        return {'User': f'{uid} UserOpenLDAP'}, 200

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


class UserListOpenLDAPResource(Resource):

    def get(self):
        return {'User': 'UserOpenLDAP'}, 200

    def post(self):
        pass
