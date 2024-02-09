from flask import Flask, json
from flask_restful import Api
from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from backend.api.celery.celery_app import celery_init_app
from backend.api.common.regex_converter import RegexConverter
from backend.api.resources.auth_open_ldap import AuthOpenLDAP
from backend.api.resources.group_open_ldap import GroupOpenLDAPResource, GroupListOpenLDAPResource
from backend.api.resources.user_open_ldap import (UserOpenLDAPResource,
                                                  UserListOpenLDAPResource,
                                                  UserMeOpenLDAPResource, FreeIdsOpenLDAPResource)
from backend.api.db.database import db
from backend.api.config import settings

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.from_object('backend.api.config.settings')  # or this
# app.config.from_envvar('APPLICATION_SETTINGS') # or this - export APPLICATION_SETTINGS=$PWD/config/settings.py

api = Api(app)

# Cross Origin Resource Sharing
cors = CORS(app, resources={r'/api/*': {"origins": "*"}})
# cors = CORS(
#     app,
#     resources={r'/api/*': {"origins": "*"}},
#     allow_header=['Content-Type', 'Authorization']
# )

route = '/api/v1'
regex = 'regex("[a-zA-Z0-9_-]+")'

# Users resource
api.add_resource(UserMeOpenLDAPResource,  f'{route}/users/me/')
api.add_resource(UserOpenLDAPResource,  f'{route}/users/<{regex}:username_uid>')
api.add_resource(UserListOpenLDAPResource, f'{route}/users')

api.add_resource(FreeIdsOpenLDAPResource, f'{route}/free-ids')

# Group resource
api.add_resource(GroupOpenLDAPResource, f'{route}/groups/<{regex}:type_group>/<{regex}:username_cn>')
api.add_resource(GroupListOpenLDAPResource, f'{route}/groups/<{regex}:type_group>')

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

if settings.DEVELOPMENT and  __name__ == '__main__':  # Comment when prod
    app.run(debug=settings.DEBUG)  # Comment when prod


'''
If token is expired database will cleaned
database orm flask_sqlachemy
'''