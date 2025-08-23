import os
import pathlib

DEBUG = bool(int(os.environ.get('DEBUG', 1)))

SECRET_KEY = os.getenv('SECRET_KEY')

UPLOAD_FOLDER = 'files/uploads'
GLOBAL_UPLOAD_FOLDER = f'/api/v1/{UPLOAD_FOLDER}'
ABSPATH_UPLOAD_FOLDER = os.path.join(os.path.abspath('.'), UPLOAD_FOLDER)

pathlib.Path(ABSPATH_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'svg', 'webp', 'bmp', 'gif')

ITEMS_PER_PAGE = 20
SEARCH_OUTPUT_ATTRIBUTES = ["uid", "cn", "sn", "gidNumber", "uidNumber"]
SEARCH_FIELDS = [
    'cn', 'street', 'mail', 'sn',
    'st', 'givenName', 'displayName',
    'uidNumber', 'gidNumber', 'postalCode',
    'loginShell', 'homeDirectory'
]
GROUP_SEARCH_FIELDS = [
    'cn', 'gidNumber', "memberUid"
]


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '0.0.0.0')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
POSTGRES_DB = os.getenv('POSTGRES_DB')

SQLALCHEMY_DATABASE_URI = (f'postgresql://{POSTGRES_USER}:'
                           f'{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_USERNAME = os.getenv('REDIS_USERNAME')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_SSL = bool(int(os.getenv('REDIS_SSL', 0)))
REDIS_SSL_CERTFILE = os.getenv('REDIS_SSL_CERTFILE')
REDIS_SSLKEYFILE = os.getenv('REDIS_SSLKEYFILE')
REDIS_SSL_CA_CERTS = os.getenv('REDIS_SSL_CA_CERTS')
