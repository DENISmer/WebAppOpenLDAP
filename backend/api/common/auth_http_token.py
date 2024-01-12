from flask_httpauth import HTTPTokenAuth

from backend.api.common.token_manager import TokenManager

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    is_token = TokenManager().check_token(token)
    if not is_token:
        return False
    return token