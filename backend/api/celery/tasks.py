import logging

from celery import shared_task

from backend.api.db.database import db
from backend.api.db.models import TokenModel
from backend.api.db.database_queries import DbQueries


@shared_task
def remove_expired_tokens():

    db_queries = DbQueries(session=db.session)
    db_queries.bulk_delete(TokenModel)

    logging.log(logging.INFO, 'Remove tokens from db')
