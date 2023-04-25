from data_collecting.reddit_posts_data_generator import post_data_generator, post_collection
from website.celery import celery
from dateutil.relativedelta import relativedelta
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from pathlib import Path
import datetime as dt
# import os

# # uses environmental variable from .env to connect to my MongoDB URI
# dotenv_path = Path('website/.env')
# load_dotenv(dotenv_path=dotenv_path)
# # connects to my mongodb uri 
# client = MongoClient(os.getenv("MONGODB_URI"))
# # sets 'db' to posts_database 
# db = client.posts_database
# post_collection = db.post_collection

@celery.task
def my_task():
    # pull posts submissions from the latest document timestamp to current time
    start_time_input = post_collection.find_one({}, sort=[('created_utc', -1)])["created_utc"]
    end_time_input = int(dt.datetime.timestamp(dt.datetime.utcnow()))
    post_data_generator(start_time_input, end_time_input)


