from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import uuid

from api.db.database import db
from api.db.database_queries import DbQueries
from api.db.models import TokenModel


class TokenManagerAbstract(ABC):

    def __init__(self, user=None):
        self.user = user

    @abstractmethod
    def create_token(self):
        pass

    @abstractmethod
    def check_token(self, token):
        pass


class TokenManagerDB(TokenManagerAbstract):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_queries = DbQueries(db.session)

    def create_token(self):
        '''
        This function creates access token
        :return token
        '''

        token = uuid.uuid4().hex
        instance = self.db_queries.get_instance(TokenModel, dn=self.user.dn)

        if instance:
            res = self.db_queries.update_instance(
                instance,
                token=token,
                datetime_create=datetime.utcnow(),
                role=self.user.role,
                userPassword=self.user.userPassword
            )
        else:
            res = self.db_queries.create_instance(
                TokenModel,
                dn=self.user.dn,
                token=token,
                uid=self.user.uid,
                role=self.user.role,
                userPassword=self.user.userPassword
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
            'role': instance.role,
            'userPassword': instance.userPassword
        }


class Token:
    def __init__(self, token):
        self.token = token
