from dotenv import  load_dotenv
import os


load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_USERNAME = os.getenv('REDIS_USERNAME')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_SSL = bool(int(os.getenv('REDIS_SSL', 0)))
REDIS_SSL_CERTFILE = os.getenv('REDIS_SSL_CERTFILE')
REDIS_SSLKEYFILE = os.getenv('REDIS_SSLKEYFILE')
REDIS_SSL_CA_CERTS = os.getenv('REDIS_SSL_CA_CERTS')
