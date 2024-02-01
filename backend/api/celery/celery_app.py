from celery import Celery, Task
from flask import Flask

from backend.api.celery import settings


app = Flask(__name__)


def celery_init_app(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,
                        broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
                        )
    celery_app.config_from_object('backend.api.celery.settings')
    celery_app.set_default()
    app.extensions['celery'] = celery_app

    return celery_app


celery_app = celery_init_app(app)
