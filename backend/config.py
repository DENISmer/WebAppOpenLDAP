from dotenv import load_dotenv
import os


load_dotenv()

CERT_FILE = os.getenv('CERT_FILE')
HOSTS = os.getenv('HOST').split(',')
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')