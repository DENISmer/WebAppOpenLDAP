from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    print('Confirm token')
    print('Token -', token)
    return token