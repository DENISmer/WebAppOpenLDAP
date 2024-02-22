from flask_httpauth import HTTPTokenAuth

from backend.api.common.token_manager import TokenManagerDB
from backend.api.config import settings
from backend.api.common.roles import Role

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
            'role': Role.WEB_ADMIN.value,
            'userPassword': b'gAAAAABlyam-qUrcndMw05tw6sCpLvCVucmni3MKeZhEN7Be7Sqn7V2KlfWcIgj3gg5Apx7e9H1yIJfEJ4psvcsdnkrnxAhLEw==',
        }

    return is_token


@auth.error_handler
def auth_error(status):
    if status == 401:
        return {'message': 'Unauthorized Access', 'status': status}, status
    else:
        return {'message': 'Insufficient access rights', 'status': status}, status

