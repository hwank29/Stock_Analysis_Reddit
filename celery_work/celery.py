from flask_app.data_collecting.reddit_posts_data_generator import post_collection, post_data_generator
from celery import Celery
from celery.schedules import crontab
from time import sleep
import datetime as dt
import os 

redis_ip = os.environ.get('REDIS_IP')

# start celery
celery = Celery('tasks', backend=f'redis://{redis_ip}:6379/1', broker=f'redis://{redis_ip}:6379/0')

@celery.task
def my_task():
    # pull recent posts submissions and insert data into MongoDB
    post_data_generator()

celery.conf.timezone = 'UTC'

# background task every 2 hours
celery.conf.beat_schedule = {
    'run-my-task-every-2-hour': {
        'task': 'celery_work.celery.my_task',
        'schedule': crontab(minute='0', hour='*/2')
    },
}

# celery -A celery_work.celery beat -l info
# celery -A celery_work.celery worker -l info

# pkill -f "celery beat"
# pkill -f "celery worker"


