from typing import Union

from sqlalchemy.exc import IntegrityError

from backend.api.db.models import Token


class DbQueries:
    def __init__(self, session):
        self.session = session

    def get_item(self, model, **kwargs) -> Union[Token, None]:
        item = self.session.query(model).filter_by(**kwargs).one_or_none()
        return item

    def get_or_create(self, model, **kwargs):
        item = self.get_item(model, **kwargs)
        if not item:
            pass

        # from backend.api.db.database import db
        # from backend.api.db.models import Token
        # item = db.session.query(Token).filter(Token.dn == 'user.dn').one_or_none()
        #
        # if not item:
        #     try:
        #         token = Token(
        #             dn=user.dn,
        #             token='sdfsdfwfwsdfsdf'
        #         )
        #         db.session.add(token)
        #         db.session.commit()
        #     except Exception as e:
        #         print(e)
        #         db.session.rollback()

        return item