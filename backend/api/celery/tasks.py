import logging
from datetime import datetime, timedelta

from celery import shared_task

from backend.api.db.database import db
from backend.api.db.models import TokenModel
from backend.api.db.database_queries import DbQueries

from sqlalchemy import func


@shared_task()
def remove_expired_tokens():

    db_queries = DbQueries(session=db.session)
    current_datetime = datetime.utcnow()
    filter_del = (TokenModel.datetime_create < current_datetime - timedelta(days=1))  # func.DATETIME(...)
    db_queries.bulk_delete(TokenModel, filter_del=filter_del)
    logging.log(logging.INFO, 'Remove tokens from db {0}'.format(datetime.now()))
