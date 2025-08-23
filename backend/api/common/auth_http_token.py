from flask_httpauth import HTTPTokenAuth

from api.common.token_manager import TokenManagerDB


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):

    auth_token = TokenManagerDB().check_token(token)
    if not auth_token:
        return False

    return auth_token


@auth.error_handler
def auth_error(status):
    if status == 401:
        return {'message': 'Unauthorized Access', 'status': status}, status
    else:
        return {'message': 'Insufficient access rights', 'status': status}, status
