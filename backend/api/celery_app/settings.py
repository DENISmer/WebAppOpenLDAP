import os
from dotenv import load_dotenv


load_dotenv()

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
result_backend = os.getenv('CELERY_RESULT_BACKED', 'redis://localhost:6379/1')
task_ignore_result = True
broker_connection_retry_on_startup = True

imports = (
    'api.celery_app.tasks',
)

TIMES_SCHEDULE = {
    'TIME_REMOVE_EXPIRED_TOKENS': 10.0 * 6 * 10,
}
