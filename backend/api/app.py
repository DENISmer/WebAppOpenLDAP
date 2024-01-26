from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from backend.api.resources.auth_open_ldap import AuthOpenLDAP
from backend.api.resources.group_open_ldap import GroupOpenLDAPResource, GroupListOpenLDAPResource
from backend.api.resources.user_open_ldap import (UserOpenLDAPResource,
                                                  UserListOpenLDAPResource,
                                                  UserMeOpenLDAPResource)

app = Flask(__name__)
app.config.from_object('backend.api.config.settings') # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)

# Cross Origin Resource Sharing
cors = CORS(app, resources={r'/users': {'origins': '*'}})


# Users resource
api.add_resource(UserMeOpenLDAPResource,  '/users/me/')
api.add_resource(UserOpenLDAPResource,  '/users/<string:username_uid>')
api.add_resource(UserListOpenLDAPResource, '/users')

# Group resource
api.add_resource(GroupOpenLDAPResource, '/groups/<string:type_group>/<string:username_cn>')
api.add_resource(GroupListOpenLDAPResource, '/groups/<string:type_group>')

# Auth resource
api.add_resource(AuthOpenLDAP, '/auth/token')


# Error

if __name__ == '__main__':
    app.run(debug=True)


# receive dn
# performs rebind
# make the best schema with pool connection
'''
If token is expired database clean
database orm flask_sqlachemy
'''