import os
from dotenv import load_dotenv


load_dotenv()

BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKED', 'redis://localhost:6379/1')
CELERY_IGNORE_RESULT = True

CELERY_IMPORTS = (
    'backend.api.celery.tasks',
)

TIMES_SCHEDULE = {
    'TIME_REMOVE_EXPIRED_TOKENS': 10.0 * 6 * 10,
}
