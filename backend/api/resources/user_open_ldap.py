from flask_restful import Resource


class UserOpenLDAPResource(Resource):

    def list(self):
        return {'User': 'UserOpenLDAP'}

    def get(self, uid):
        return {'User': f'{uid} UserOpenLDAP'}

    def post(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass
