import jwt
import time
import uuid
import logging

from backend.api.common.exceptions import UserIsNone
from backend.api.common.user_manager import User
from backend.api.config import settings


class TokenManager:
    def __init__(self, user: User = None):
        self.user = user

    def create_token(self):
        '''
        This function creates access token
        :return token
        '''

        if not self.user:
            raise UserIsNone('Not user')

        token = jwt.encode(
            {
                'dn': self.user.dn,
                'uid': self.user.uid,
                'admin': self.user.is_admin,
                'exp': int(time.time()) + 3600,
                'jti': f'{uuid.uuid4()}',
            },  # payload
            settings.SECRET_KEY,  # private key
            algorithm=settings.ALGORITHMS,  # algorithm
        )
        return token

    def check_token(self, token) -> bool:
        '''
        This function check access token
        :param token: is used to check valid
        :return data: extracted from token or False
        '''

        try:
            data = jwt.decode(
                token,  # token
                settings.SECRET_KEY,  # private key
                algorithms=settings.ALGORITHMS,  # algorithm
            )
        except Exception as e:
            logging.log(logging.ERROR, f'e: {e}')
            return False

        return data


class Token:
    def __init__(self, token):
        self.token = token
