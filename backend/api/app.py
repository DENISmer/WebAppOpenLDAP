
import json

from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from api.common.regex_converter import RegexConverter
from api.resourses.auth_open_ldap import AuthOpenLDAPResource
from api.resourses.user_open_ldap import UserOpenLDAPResource, UserListOpenLDAPResource
from api.resourses.group_open_ldap import GroupOpenLDAPResource, GroupListOpenLDAPResource
from api.resourses.file_open_ldap import FileUploadsOpenLDAPResource, FileOpenLDAPResource
from api.managers.ldap_manager import ldap_manager
from api.db.database import db


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.config.from_object("api.conf.settings")


print(f"id ldapmanager app: {id(ldap_manager)}")

# Cross Origin Resource Sharing
# cors = CORS(app, resources={r'/api/*': {"origins": "*"}})
cors = CORS(
    app,
    resources={r'/api/*': {"origins": "*"}},
    allow_header=['Content-Type', 'Authorization']
)


api_spec_url = '/docs/swagger'
api = Api(
    app,
    api_version='v1.0',
    api_spec_url=api_spec_url,
    add_api_spec_resource=True,
    contact={
        "name": "API Support",
        "email": "serbinovichgs@ict.nsc.ru"
    },
    title="REST API WebAppOpenLDAP application",
    description="The service is used to manage OpenLDAP using LDAP protocol",
    security_definitions={
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Input example: \"Bearer \<Your token\>\""
        }
    },
    schemes=["http", "https"]
)

regex = 'regex("[a-zA-Z0-9_-]+")'
regex_files = 'regex("[a-zA-Z0-9_-]+\.[a-zA-Z]+")'

api.add_resource(FileOpenLDAPResource, f'/api/v1/files/<{regex}:uid>')
api.add_resource(FileUploadsOpenLDAPResource, f'/api/v1/files/uploads/<{regex_files}:name>')

api.add_resource(GroupOpenLDAPResource, f"/api/v1/groups/<{regex}:cn>")
api.add_resource(GroupListOpenLDAPResource, f"/api/v1/groups")

api.add_resource(UserOpenLDAPResource, f"/api/v1/users/<{regex}:uid>")
api.add_resource(UserListOpenLDAPResource, f"/api/v1/users")

api.add_resource(AuthOpenLDAPResource, f"/api/v1/auth/token")

# Database init
db.init_app(app)

# database create table
with app.app_context():
    db.create_all()

# Swagger
SWAGGER_URL = api_spec_url
API_URL = f"{api_spec_url}.json"

with app.app_context():
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Swagger UI"
        }
    )

app.register_blueprint(swagger_ui_blueprint)


# Error
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


if __name__ == "__main__":
    app.run(debug=True)

