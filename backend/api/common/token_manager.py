import jwt
import time

from flask import abort

from backend.api.common.exceptions import UserIsNone
from backend.api.common.user_manager import User
from backend.api.config import settings


class TokenManager:
    def __init__(self, user: User = None):
        self.user = user

    def create_token(self):
        ''' This function creates access token '''

        if not self.user:
            raise UserIsNone('Not user')

        token = jwt.encode(
            {
                'dn': self.user.dn,
                'uid': self.user.uid,
                'exp': int(time.time()) + 3600,
            }, # payload
            settings.SECRET_KEY, # private key
            algorithm=settings.ALGORITHMS, # algorithm
        )
        return token

    def check_token(self, token) -> bool:
        ''' This function check access token '''

        try:
            data = jwt.decode(
                token, # token
                settings.SECRET_KEY, # private key
                algorithms=settings.ALGORITHMS, # algorithm
            )
        except:
            return False

        return data
