import os
from dotenv import load_dotenv

load_dotenv()

# Config app

SECRET_KEY = 'secret'

DEBUG = True

ALGORITHMS = 'HS256'

NOT_AUTH = True

ITEMS_PER_PAGE = 20


FILE_DB_NAME = 'proj.db'
# DATABASE URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///{FILE_DB_NAME}'

CERT_FILE_LDAP = os.getenv('CERT_FILE')
HOSTS = os.getenv('LDAP_HOSTS').split(',')
LDAP_PORT = int(os.getenv('LDAP_PORT'))