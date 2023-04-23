from data_collecting.reddit_posts_data_generator import client, post_collection, post_data_generator
from website.celery import celery

from dateutil.relativedelta import relativedelta
import datetime as dt


@celery.task
def my_task():
    # pull posts submissions every 12 hours from r/stocks
    start_time_input = int(dt.datetime.timestamp(dt.datetime.utcnow() - relativedelta(hours=12)))
    end_time_input = int(dt.datetime.timestamp(dt.datetime.utcnow()))
    post_data_generator(start_time_input, end_time_input)


