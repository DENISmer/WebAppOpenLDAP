from flask_httpauth import HTTPTokenAuth

from backend.api.common.token_manager import TokenManagerDB
from backend.api.config import settings


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):

    if not settings.NOT_AUTH:
        is_token = TokenManagerDB().check_token(token)
        if not is_token:
            return False
    else:
        is_token = {
            'dn': 'uid=bob,ou=People,dc=example,dc=com',
            'uid': 'bob',
            'role': 'webadmins',
        }

    return is_token


@auth.error_handler
def auth_error(status):
    return {'token': 'expired', 'status': status}, status

