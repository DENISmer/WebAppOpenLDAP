from flask_restful import Resource

from backend.api.common.auth_http_token import auth
from backend.api.common.roles import Role


class GroupOpenLDAPResource(Resource):

    @auth.login_required(role=[Role.WEBADMIN])
    def get(self, *args, **kwargs):
        pass

    @auth.login_required(role=[Role.WEBADMIN])
    def put(self, *args, **kwargs):
        pass

    @auth.login_required(role=[Role.WEBADMIN])
    def patch(self, *args, **kwargs):
        pass


class GroupListOpenLDAPResource(Resource):

    @auth.login_required(role=[Role.WEBADMIN])
    def get(self, *args, **kwargs):
        pass

    @auth.login_required(role=[Role.WEBADMIN])
    def post(self, *args, **kwargs):
        pass
