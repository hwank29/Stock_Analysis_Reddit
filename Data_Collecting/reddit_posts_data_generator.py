from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import datetime as dt
import nltk
import string
import json
import csv
import re
import os 
import csv
import time
from dotenv import load_dotenv
from pymongo import MongoClient

# connects to my mongodb uri 
client = MongoClient(os.getenv("MONGODB_URI"))
# sets 'db' to posts_database 
db = client.posts_database
post_collection = db.post_collection

# Organize company name and ticker dictionaries 
with open('data/S&P500_tickers_names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    ticker_name_dict = {}
    company_name_dict = {}
    company_capitalize_dict = {}
    ticker_capitalize_dict = {}
    company_ticker_dict = {}
    for company in csv_reader:
        ticker_name_dict[company['Ticker'].lower()] = 0
        company_name_dict[company['Name'].lower()] = 0 
        company_capitalize_dict[company['Name'].lower()] = company['Name']
        ticker_capitalize_dict[company['Ticker'].lower()] = company['Ticker']
        company_ticker_dict[company['Name'].lower()]= company['Ticker'].lower() 

# Data cleaning unneccessary parts of selftext 
def cleaning(text):    
    text = text.lower()
    # Removes http and www website url
    text = re.sub('http\w+|www\.\S+', "", text)
    # Removes special characters
    text = re.sub('<.*?>+', "", text)
    # Removes digits
    text = re.sub("\d+", "", text)
    # Removes tap and white space
    text = re.sub("\s\s+", " ", text)
    # Removes punctuation besides $ for ticker 
    text = text.translate(str.maketrans('', '', string.punctuation.replace('$','') + '’'))
    text_tokenize = word_tokenize(text)
    # Make a list variable for words that are not actually mentioned as tickers but give misinformation 
    new_stop_words = ['low', 'dow', 'see', 'k', 'amp', 'well', 'im', 'tech', 'key', 'peak', 'fast', 'hes', 'dd', 'factset', 'cost']
    # Makes a variable for stop words and remove any stop words from column title and selftext
    stop_words = nltk.corpus.stopwords.words('english')
    stop_words.extend(new_stop_words)
    text = " ".join([t for t in text_tokenize if not t in stop_words])
    return text

three_years_from_today_epoch = dt.datetime.timestamp(dt.datetime.now() - relativedelta(years=3))
today_epoch = dt.datetime.timestamp(dt.datetime.now())

# Function to generate data of posts in 'stocks' subreddit and input the post data into post_collection(mongodb)
# 'start_time' and 'end_time' are on epoch time
def post_data_generator(start_time, end_time):
    # if first time (developer), needs to put 3 years of reddit post data into mongodb database; may take some time
    if post_collection.count_documents({}) == 0:
        # recurse until 3 years of reddit post data are inputted 
        while True:
            start_date_input = three_years_from_today_epoch
            # https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
            # Can pull 1000 reddit posts per request at max so loop to get every post
            post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_date_input}&before={today_epoch}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,upvote_ratio,selftext'
            def get(uri):
                response = urlopen(uri)
                return json.loads(response.read())
            posts = get(post_data_generator_uri)
            # loop to store reddit post data 
            for post in posts['data']:
                if post['selftext'] != '[removed]' and post:
                    post_document = {'id': post['id'], 
                                'utc_datetime_str' : post['utc_datetime_str'],
                                'created_utc' : post['created_utc'], 
                                'title': cleaning(post['title']),
                                'score': post['score'],
                                'upvote_ratio': post['upvote_ratio'],
                                'selftext': cleaning(post['selftext'])}
                    post_collection.insert_one(post_document)

        # recurse until there is no more posts between 'before' and 'after' time 
            if posts['data']:
                start_date_input = post_collection.find().sort({"created_utc": -1}).limit(1)
            else:
                break
        return 
    
    # when the end_date is greater than the currently inputted document 
    elif end_time > post_collection.find().sort({"created_utc": -1}).limit(1):
        while True:
            # https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
            # Can pull 1000 reddit posts per request at max so loop to get every post
            post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={end_time}&before={post_collection.find().sort({"created_utc": -1}).limit(1)}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,upvote_ratio,selftext'
            def get(uri):
                response = urlopen(uri)
                return json.loads(response.read())
            posts = get(post_data_generator_uri)

            # loop to store reddit post data 
            for post in posts['data']:
                if post['selftext'] != '[removed]' and post:
                    post_document = {'id': post['id'], 
                                'utc_datetime_str' : post['utc_datetime_str'],
                                'created_utc' : post['created_utc'], 
                                'title': cleaning(post['title']),
                                'score': post['score'],
                                'upvote_ratio': post['upvote_ratio'],
                                'selftext': cleaning(post['selftext'])}
                    post_collection.insert_one(post_document)

        # recurse until there is no more posts between 'before' and 'after' time 
            if posts['data']:
                start_date_input = post_collection.find().sort({"created_utc": -1}).limit(1)
            else:
                break
        return

# # Count ticker or company names mentioned in each post(a post can mention the same company name multple times, so one count per post)
# for text in post_data['selftext']:
#     for word in word_tokenize(text):
#         if word in list(ticker_name_dict.keys()):
#             ticker_name_dict[word] += 1
#         elif word in list(company_name_dict.keys()):
#             company_name_dict[word] += 1
            
# # sums up the number of times a company is mentioned by name and ticker
# company_mentioned_together = company_name_dict.copy()
# for key, value in company_ticker_dict.items():
#     company_mentioned_together[key] += ticker_name_dict[value]
# company_mentioned_together = {key: value for key, value in sorted(company_mentioned_together.items(), key=lambda item: item[1], reverse=True)}    

# name_list, ticker_list, mentioned_num = [], [], []

# for key, value in company_mentioned_together.items():
#     name_list.append(company_capitalize_dict[key])
#     ticker_list.append(ticker_capitalize_dict[company_ticker_dict[key]])
#     mentioned_num.append(value)

# # rank top 25 most mentioned stops
# data_mentioned_stock = {
#     'Name' : name_list[:25],
#     'Ticker' : ticker_list[:25],
#     'Mentioned' : mentioned_num[:25],
#     'Highest' : [],
#     'Lowest' : [],
#     'Change vs S&P500': [],
# } 
