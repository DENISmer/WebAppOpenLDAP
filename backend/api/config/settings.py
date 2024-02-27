import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

# Config app

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(int(os.environ.get('DEBUG', 1)))
DEVELOPMENT = bool(int(os.environ.get('DEVELOPMENT', 1)))

ALGORITHMS = 'HS256'

NOT_AUTH = bool(int(os.environ.get('NOT_AUTH', 1)))

ITEMS_PER_PAGE = 20

UPLOAD_FOLDER = 'files/uploads'
GLOBAL_UPLOAD_FOLDER = f'/api/v1/{UPLOAD_FOLDER}'
ABSPATH_UPLOAD_FOLDER = os.path.join(os.path.abspath('.'), UPLOAD_FOLDER)
pathlib.Path(ABSPATH_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'webp', 'bmp', 'gif'}

FILE_DB_NAME = os.getenv('FILE_DB_NAME')
# DATABASE URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///{FILE_DB_NAME}'

CERT_FILE_LDAP = os.getenv('CERT_FILE')
HOSTS = os.getenv('LDAP_HOSTS', '0.0.0.0').split(',')
LDAP_PORT = int(os.getenv('LDAP_PORT'))
LDAP_USE_SSL = bool(int(os.environ.get('LDAP_USE_SSL', 0)))
