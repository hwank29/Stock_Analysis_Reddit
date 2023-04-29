from data_collecting.reddit_posts_data_generator import post_data_generator, post_collection
from website.celery import celery
import datetime as dt

@celery.task
def my_task():
    # pull posts submissions from the latest document timestamp to current time
    start_time_input = post_collection.find_one({}, sort=[('created_utc', -1)])["created_utc"]
    end_time_input = int(dt.datetime.timestamp(dt.datetime.utcnow()))
    post_data_generator(start_time_input, end_time_input)


