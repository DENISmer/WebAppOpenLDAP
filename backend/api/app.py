from flask import Flask, jsonify, json
from flask_restful import Api
from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from backend.api.celery.celery_app import celery_init_app
from backend.api.resources.auth_open_ldap import AuthOpenLDAP
from backend.api.resources.group_open_ldap import GroupOpenLDAPResource, GroupListOpenLDAPResource
from backend.api.resources.user_open_ldap import (UserOpenLDAPResource,
                                                  UserListOpenLDAPResource,
                                                  UserMeOpenLDAPResource)
from backend.api.db.database import db


app = Flask(__name__)
app.config.from_object('backend.api.config.settings')  # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)

# Cross Origin Resource Sharing
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

route = '/api/v1'

# Users resource
api.add_resource(UserMeOpenLDAPResource,  f'{route}/users/me/')
api.add_resource(UserOpenLDAPResource,  f'{route}/users/<string:username_uid>')
api.add_resource(UserListOpenLDAPResource, f'{route}/users')

# Group resource
api.add_resource(GroupOpenLDAPResource, f'{route}/groups/<string:type_group>/<string:username_cn>')
api.add_resource(GroupListOpenLDAPResource, f'{route}/groups/<string:type_group>')

# Auth resource
api.add_resource(AuthOpenLDAP, f'{route}/auth/token')

# Error


# Database init
db.init_app(app)

# database create table
with app.app_context():
    db.create_all()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "status": e.code,
        "error": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response


celery_app = celery_init_app(app)

if __name__ == '__main__':
    app.run(debug=True)


'''
If token is expired database will cleaned
database orm flask_sqlachemy
'''