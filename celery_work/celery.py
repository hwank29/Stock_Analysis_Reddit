from flask_app.data_collecting.reddit_posts_data_generator import post_collection, post_data_generator
from celery import Celery
from celery.schedules import crontab
import datetime as dt


celery = Celery('tasks', backend='redis://redis:6379/1', broker='redis://redis:6379/0')

@celery.task
def my_task():
    # pull posts submissions from the latest document timestamp to current time
    start_time_input = post_collection.find_one({}, sort=[('created_utc', -1)])["created_utc"]
    end_time_input = int(dt.datetime.timestamp(dt.datetime.utcnow()))

    post_data_generator(start_time_input, end_time_input)

print()
celery.conf.timezone = 'UTC'

# background task every one hour
celery.conf.beat_schedule = {
    'run-my-task-every-1-hour': {
        'task': 'celery_work.celery.my_task',
        'schedule': crontab(hour='*/1')
    },
}

# celery -A celery_work.celery beat -l info
# celery -A celery_work.celery worker -l info

# pkill -f "celery beat"
# pkill -f "celery worker"


