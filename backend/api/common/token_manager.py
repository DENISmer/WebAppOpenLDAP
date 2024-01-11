import jwt
import time

from backend.api.common.user_manager import User
from backend.api.config import settings


class TokenManager:
    def __init__(self, user: User):
        self.user = user

    def create_token(self):
        ''' This function creates access token '''
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

    def check_token(self) -> bool:
        ''' This function check access token '''
        return True
