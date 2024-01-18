from flask_httpauth import HTTPTokenAuth

from backend.api.common.token_manager import TokenManager
from backend.api.config import settings


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    if not settings.NOT_AUTH:
        is_token = TokenManager().check_token(token)
        if not is_token:
            return False
    else:
        is_token = {
            'dn': 'uid=test,ou=People,dc=example,dc=com',
            'uid': 'test',
            'admin': True,
        }
    return is_token
