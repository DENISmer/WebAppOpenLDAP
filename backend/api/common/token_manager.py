from datetime import datetime, timedelta

import jwt
import time
import uuid
import logging

from backend.api.common.exceptions import UserIsNone
from backend.api.common.user_manager import UserLdap
from backend.api.config import settings
from backend.api.common.groups import Group


class TokenManager:
    def __init__(self, user: UserLdap = None):
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
                'role': self.user.role.value,
                'exp': datetime.utcnow() + timedelta(days=2),#int(time.time()) + 3600 * 10,
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
        except jwt.exceptions.InvalidSignatureError:
            return False
        except jwt.exceptions.DecodeError:
            return False
        except jwt.exceptions.ExpiredSignatureError:
            # clean token
            data = jwt.decode(
                token,  # token
                settings.SECRET_KEY,  # private key
                algorithms=settings.ALGORITHMS,  # algorithm
            )
            print(data['dn'], 'data')
            return False
        except Exception as e:
            logging.log(logging.ERROR, f' e: {e}')
            return False

        return data


class Token:
    def __init__(self, token):
        self.token = token
