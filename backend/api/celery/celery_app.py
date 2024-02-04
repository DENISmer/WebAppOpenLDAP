from celery import Celery, Task
from flask import Flask
import backend.api.celery.settings as settings_celery


# Init celery app
def celery_init_app(app: Flask):
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('backend.api.celery.settings')
    celery_app.set_default()

    app.extensions['celery'] = celery_app

    celery_app.conf.beat_schedule = {
        'Clear-user-access-token': {
            'task': 'backend.api.celery.tasks.remove_expired_tokens',
            'schedule': settings_celery.TIMES_SCHEDULE['TIME_REMOVE_EXPIRED_TOKENS'],
        },
    }

    return celery_app

