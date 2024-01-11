from flask import Flask
from flask_restful import Api

from backend.api.common.auth_http_token import auth
from backend.api.resources.user_open_ldap import UserOpenLDAPResource, UserListOpenLDAPResource

app = Flask(__name__)
app.config.from_object('backend.api.config.settings') # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)
# auth = HTTPTokenAuth(scheme='Bearer')


# Users resource
api.add_resource(UserOpenLDAPResource,  '/users/<string:uid>')
api.add_resource(UserListOpenLDAPResource, '/users/')


# @auth.verify_token
# def verify_token(token):
#     print('Confirm token')
#     print('Token -', token)
#     return token


@app.route('/index')
@auth.login_required
def index():
    return 'Getting index', 200


if __name__ == '__main__':
    app.run(debug=True)


