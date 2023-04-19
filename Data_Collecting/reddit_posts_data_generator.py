from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
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

# uses environmental variable from .env to connect to my MongoDB URI
dotenv_path = Path('website/.env')
load_dotenv(dotenv_path=dotenv_path)
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

three_years_from_today_epoch = int(dt.datetime.timestamp(dt.datetime.now() - relativedelta(years=3)))
today_epoch = int(dt.datetime.timestamp(dt.datetime.now()))
# Function to generate data of posts in 'stocks' subreddit and input the post data into post_collection(mongodb)
# 'start_time' and 'end_time' are on epoch time

def post_data_generator(start_time, end_time):
    # recurse until 3 years of reddit post data are inputted 
    # start_date_input = three_years_from_today_epoch
    # end_date_input = today_epoch
    while True:
        # EX: https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
        # Can pull 1000 reddit posts per request at max so loop to get every post
        # if first time (developer), needs to put 3 years of reddit post data into mongodb database; may take some time ;; better for regular usage to the user 
        # print(post_collection.count_documents({}))
        # print(end_date_input)
        # if post_collection.count_documents({}) == 0:
        # start_date_input = three_years_from_today_epoch
        post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_time}&before={end_time}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,selftext'
        # if the largest created_utc among documents in database in smaller than end_time
        # else:
        #     post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_date_input}&before={end_time}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,selftext'
        print("start")
        def get(uri):
            response = urlopen(uri)
            return json.loads(response.read())
        posts = get(post_data_generator_uri)
        # loop to store reddit post data 
        for post in posts['data']:
            # if selftext exists and no repeated document in collection
            if post['selftext'] != '[removed]' and post:
                post_document = {'id': post['id'], 
                            'utc_datetime_str' : post['utc_datetime_str'],
                            'created_utc' : post['created_utc'], 
                            'title': cleaning(post['title']),
                            'score': post['score'],
                            'selftext': cleaning(post['selftext'])}
                post_collection.update_one({"id": post_document['id']}, {"$set": post_document}, upsert=True)
        print("stop")
        # recurse until there is no more posts between 'before' and 'after' time 
        if posts['data']:
            print(end_time)
            end_time = post_collection.find_one({}, sort=[('created_utc', 1)])["created_utc"]
            print(end_time)
        # delete old documents(older than three years) for data storage efficiency
        else:
            post_collection.delete_many({"created_utc" : { "$lte" : three_years_from_today_epoch} })
            break
    # set a dataframe for reddit post data within the range of data inputted and return the dataframe
    post_df = pd.DataFrame(list(post_collection.find({ "created_utc": {"$lte": end_time, "$gte": start_time}})))
    return post_df

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
