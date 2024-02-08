import os
from dotenv import load_dotenv

load_dotenv()

# Config app

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(int(os.environ.get('DEBUG', 1)))

ALGORITHMS = 'HS256'

NOT_AUTH = bool(int(os.environ.get('NOT_AUTH', 1)))

ITEMS_PER_PAGE = 20


FILE_DB_NAME = os.getenv('FILE_DB_NAME')
# DATABASE URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///{FILE_DB_NAME}'

CERT_FILE_LDAP = os.getenv('CERT_FILE')
HOSTS = os.getenv('LDAP_HOSTS').split(',')
LDAP_PORT = int(os.getenv('LDAP_PORT'))
