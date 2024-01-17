from flask import Flask
from flask_restful import Api

from backend.api.resources.auth_open_ldap import AuthOpenLDAP
from backend.api.resources.user_open_ldap import UserOpenLDAPResource, UserListOpenLDAPResource

app = Flask(__name__)
app.config.from_object('backend.api.config.settings') # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)


# Users resource
api.add_resource(UserOpenLDAPResource,  '/users/<string:username_uid>')
api.add_resource(UserListOpenLDAPResource, '/users/')

# Auth resource
api.add_resource(AuthOpenLDAP, '/auth/token/')


# Error

if __name__ == '__main__':
    app.run(debug=True)


# receive dn
# performs rebind
# make the best schema with pool connection
