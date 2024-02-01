
import logging
from datetime import timedelta, datetime

from sqlalchemy import delete, select, func

from backend.api.db.database import db
from backend.api.db.models import TokenModel


class DbQueries:
    def __init__(self, session):
        self.session = session

    def get_instance(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).one_or_none()
        return instance

    def create_instance(self, model, **kwargs):
        instance = model(**kwargs)

        try:
            self.session.add(instance)
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
            return None

        return instance

    def update_instance(self, instance, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)

            self.session.flush()
            self.session.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            self.session.rollback()
            return None

        return instance

    def delete_instance(self, instance):
        self.session.delete(instance)

    def bulk_delete(self, model, **kwargs):
        # delete(model).where(model.datetime_create > timedelta(seconds=10))
        current_datetime = datetime.utcnow()
        selct = self.session.query(model).filter(func.DATETIME(model.datetime_create) < current_datetime - timedelta(minutes=10)).delete()
        # selct = self.session.query(model).filter_by(datetime_create=current_datetime - timedelta(seconds=10)).all()
        # selct = select(model).where(model.datetime_create + timedelta(seconds=10) < datetime.now()).all()
        # print(selct.__dict__)
        # print(selct)
        # for item in selct:
        #     print(item.uid, item.datetime_create, current_datetime, current_datetime - timedelta(seconds=10), item.datetime_create < current_datetime - timedelta(seconds=10))
        # row = self.session.execute(selct)
        # print(row)
