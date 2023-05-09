from flask_app.data_collecting.reddit_posts_data_generator import post_collection, post_data_generator
from celery import Celery
from celery.schedules import crontab
import datetime as dt

# start celery
celery = Celery('tasks', backend='redis://redis:6379/1', broker='redis://redis:6379/0')

@celery.task
def my_task():
    # pull recent posts submissions and insert data into MongoDB
    post_data_generator()

celery.conf.timezone = 'UTC'

# background task every 4 hours
celery.conf.beat_schedule = {
    'run-my-task-every-2-hour': {
        'task': 'celery_work.celery.my_task',
        'schedule': crontab(hour='*/2')
    },
}

# celery -A celery_work.celery beat -l info
# celery -A celery_work.celery worker -l info

# pkill -f "celery beat"
# pkill -f "celery worker"


