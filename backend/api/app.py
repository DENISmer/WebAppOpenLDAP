from flask import Flask
from flask_restful import Api

from backend.api.resources.user_open_ldap import UserOpenLDAPResource


app = Flask(__name__)
app.config.from_object('backend.api.config.settings') # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)


api.add_resource(UserOpenLDAPResource, '/users/', '/users/<string:uid>')

if __name__ == '__main__':
    app.run(debug=True)


