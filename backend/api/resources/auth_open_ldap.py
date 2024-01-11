from flask_restful import Resource


class AuthOpenLDAP(Resource):

    def get(self):
        pass

    def post(self): # pass and uid (it is part of the dn) check ldap.
        pass
