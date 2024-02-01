from flask import Flask, jsonify, json
from flask_restful import Api
from flask_cors import CORS

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
cors = CORS(app, resources={r'/users': {'origins': '*'}})

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


@app.errorhandler(404)
def not_found(e):
    response = jsonify({
        'message': 'The requested URL was not found on the server. '
                   'If you entered the URL manually please check your spelling and try again.',
        'error': 'Not found',
        'status': 404,
    })
    response.status = 404
    return response

# from flask import json
# from werkzeug.exceptions import HTTPException
# @app.errorhandler(HTTPException)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response


celery_app = celery_init_app(app)

if __name__ == '__main__':
    app.run(debug=True)


# receive dn
# performs rebind
# make the best schema with pool connection
'''
If token is expired database clean
database orm flask_sqlachemy
'''