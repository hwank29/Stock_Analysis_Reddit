from celery import Celery
from celery.schedules import crontab

celery = Celery('tasks', backend='redis://localhost:6379/1', broker='redis://localhost:6379/0')

celery.conf.timezone = 'UTC'

celery.conf.beat_schedule = {
    'run-my-task-every-12-hours': {
        'task': 'website.tasks.my_task',
        'schedule': crontab(hour='*/12')
    },
}

