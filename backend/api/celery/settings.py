import os
from dotenv import load_dotenv


load_dotenv()

BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')

CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKED', 'redis://localhost:6379/1')

task_ignore_result = True
