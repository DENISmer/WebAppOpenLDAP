from flask_restful import Resource, fields, marshal_with, request

from backend.api.common.token_manager import TokenManager, Token
from backend.api.common.user_manager import User

resource_field = {
    'token': fields.String
}


class AuthOpenLDAP(Resource):

    @marshal_with(resource_field)
    def get(self):
        token = TokenManager(User(dn='asdasd', uid='asdasd')).create_token()
        return Token(token=token)

    def post(self): # pass and uid (it is part of the dn) check ldap.
        pass
