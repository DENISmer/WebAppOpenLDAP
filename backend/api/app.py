from flask import Flask, json
from flask_restful import Api
from flask_cors import CORS

from werkzeug.exceptions import HTTPException

from backend.api.celery.celery_app import celery_init_app
from backend.api.common.regex_converter import RegexConverter
from backend.api.common.route import Route
from backend.api.redis.redis_storage import RedisStorage
from backend.api.resources.auth_open_ldap import AuthOpenLDAP
from backend.api.resources.files_open_ldap import (FileDownloadOpenLDAPResource,
                                                   FileUploadOpenLDAPResource)
from backend.api.resources.group_open_ldap import (GroupOpenLDAPResource,
                                                   GroupListOpenLDAPResource)
from backend.api.resources.user_open_ldap import (UserOpenLDAPResource,
                                                  UserListOpenLDAPResource,
                                                  UserMeOpenLDAPResource)
from backend.api.resources.free_id_open_ldap import FreeIdsOpenLDAPResource
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
regex_files = 'regex("[a-zA-Z0-9_-]+\.[a-zA-Z]+")'

# Users resource
api.add_resource(UserMeOpenLDAPResource,  f'{route}/{Route.USERS.value}/me/')
api.add_resource(UserOpenLDAPResource,  f'{route}/{Route.USERS.value}/<{regex}:username_uid>')
api.add_resource(UserListOpenLDAPResource, f'{route}/{Route.USERS.value}')

# Files resource
api.add_resource(FileUploadOpenLDAPResource,  f'{route}/{Route.FILES.value}/upload/<{regex}:username_uid>')
api.add_resource(FileDownloadOpenLDAPResource,  f'{route}/{Route.FILES.value}/download/<{regex_files}:name>')

# Free ids
api.add_resource(FreeIdsOpenLDAPResource, f'{route}/free-ids')

# Group resource
api.add_resource(GroupOpenLDAPResource, f'{route}/{Route.GROUPS.value}/<{regex}:type_group>/<{regex}:username_uid>')
api.add_resource(GroupListOpenLDAPResource, f'{route}/{Route.GROUPS.value}/<{regex}:type_group>')

# Auth resource
api.add_resource(AuthOpenLDAP, f'{route}/{Route.AUTH.value}/token')

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

RedisStorage().remove_all()

if settings.DEVELOPMENT and __name__ == '__main__':  # Comment when prod
    app.run(debug=settings.DEBUG)  # Comment when prod


'''
If token is expired database will cleaned
database orm flask_sqlachemy
'''