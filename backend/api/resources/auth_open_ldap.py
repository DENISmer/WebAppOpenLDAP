from flask_restful import Resource, fields, marshal_with, request

resource_field = {
    'token': fields.String
}


class AuthOpenLDAP(Resource):

    @marshal_with(resource_field)
    def get(self):
        return {'Auth': 'AuthOpenLDAP'}

    def post(self): # pass and uid (it is part of the dn) check ldap.
        pass
