import os
from dotenv import load_dotenv

load_dotenv()

# Config app

SECRET_KEY = 'secret'

DEBUG = True

ALGORITHMS = 'HS256'

NOT_AUTH = False

ITEMS_PER_PAGE = 2


FILE_DB_NAME = 'proj.db'
# DATABASE URI
SQLALCHEMY_DATABASE_URI = f'sqlite:///{FILE_DB_NAME}'
