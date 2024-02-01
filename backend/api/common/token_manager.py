from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import jwt
import uuid
import logging

from backend.api.common.exceptions import UserIsNone
from backend.api.config import settings

from backend.api.db.database import db
from backend.api.db.database_queries import DbQueries
from backend.api.db.models import TokenModel


class TokenManagerAbstract(ABC):

    def __init__(self, user=None):
        self.user = user

    @abstractmethod
    def create_token(self):
        pass

    @abstractmethod
    def check_token(self, token):
        pass


class TokenManagerJWT(TokenManagerAbstract):

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
            return False
        except Exception as e:
            logging.log(logging.ERROR, f' e: {e}')
            return False

        return data


class TokenManagerDB(TokenManagerAbstract):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_queries = DbQueries(db.session)

    def create_token(self):
        '''
        This function creates access token
        :return token
        '''

        instance = self.db_queries.get_instance(TokenModel, dn=self.user.dn)
        # self.db_queries.bulk_delete(TokenModel)
        token = uuid.uuid4().hex
        if instance:
            res = self.db_queries.update_instance(
                instance,
                token=token,
                datetime_create=datetime.utcnow(),
            )
        else:
            res = self.db_queries.create_instance(
                TokenModel,
                dn=self.user.dn,
                token=token,
                uid=self.user.uid,
                role=self.user.role.value,
            )

        if not res:
            token = None

        return token

    def check_token(self, token):
        '''
        This function check access token
        :param token: is used to check valid
        :return data: extracted from token or False
        '''

        instance = self.db_queries.get_instance(TokenModel, token=token)

        if not instance:
            return False

        return {
            'dn': instance.dn,
            'uid': instance.uid,
            'role': instance.role
        }


class Token:
    def __init__(self, token):
        self.token = token
