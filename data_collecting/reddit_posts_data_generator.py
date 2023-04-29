from data_collecting.analyze_reddit_data import analyze_stock, sentiment_measure
from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import datetime as dt
import socket 
import string
import json
import csv
import re
import os 
import csv

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
    company_ticker_dict = {}
    for company in csv_reader:
        ticker_name_dict[company['Ticker'].lower()] = 0
        company_name_dict[company['Name'].lower()] = 0 
        company_capitalize_dict[company['Name'].lower()] = company['Name']
        company_ticker_dict[company['Name'].lower()]= company['Ticker'].lower() 

# Data cleaning unneccessary parts of selftext 
def cleaning(text):    
    text = text.lower()
    # Removes http and www website url
    text = re.sub('^https?://', "", text)
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
    new_stop_words = ['low', 'dow', 'see', 'k', 'amp', 'well', 'im', 'tech', 'key', 'peak', 'fast', 'hes', 'dd', 'factset', 'cost', 'share', 'shares', 'per', 'dont', 'any', 'one', '']
    # Makes a variable for stop words and remove any stop words from column title and selftext
    stop_words = stopwords.words('english')
    stop_words.extend(new_stop_words)
    text = " ".join([t for t in text_tokenize if not t in stop_words])
    return text

# counts stocks/tickers mentioned in each post
def name_counter(selftext):
    ticker_dict_copy = ticker_name_dict.copy()
    company_dict_copy = company_name_dict.copy()
    company_ticker_dict_copy = company_ticker_dict.copy()

    # Count ticker or company names mentioned in each post(a post can mention the same company name multple times, so one count per post)
    for word in word_tokenize(selftext):
        if word in list(ticker_dict_copy.keys()):
            ticker_dict_copy[word] += 1
        elif word in list(company_dict_copy.keys()):
            company_dict_copy[word] += 1
    # sums up the number of times a company is mentioned by name and ticker
    company_mentioned_together = company_dict_copy.copy()
    for key, value in company_ticker_dict_copy.items():
        company_mentioned_together[key] += ticker_name_dict[value]
    company_mentioned_together = {key: value for key, value in sorted(company_mentioned_together.items(), key=lambda item: item[1], reverse=True)}    
    
    name_list, mentioned_num = [], []
    for key, value in company_mentioned_together.items():
        name_list.append(key)
        mentioned_num.append(value)
    
    return [name_list, mentioned_num]

# if first time using 
two_years_from_today_epoch = int(dt.datetime.timestamp(dt.datetime.utcnow() - relativedelta(years=2)))
today_epoch = int(dt.datetime.timestamp(dt.datetime.utcnow()))
# function to generate data of posts in 'stocks' subreddit and input the post data into post_collection(mongodb)
def post_data_generator(start_time, end_time):
    """if first time using"""
    # start_time_input = two_years_from_today_epoch
    # end_time_input = today_epoch 
    start_time_input = start_time
    end_time_input = end_time
    latest_time_doc = 0
    while True:
        try:
            # EX: https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
            # can pull 1000 reddit posts per request at max so loop to get every post
            # if first time (developer), needs to put 3 years of reddit post data into mongodb database; may take some time ;; better for regular usage to the user 
            post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_time_input}&before={end_time_input}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,selftext'
            print("start")
            def get(uri):
                response = urlopen(uri, timeout=10)
                print("get uri")
                return json.loads(response.read())
            posts = get(post_data_generator_uri)
            # loop to store reddit post data 
            for post in posts['data']:
                # if selftext exists and no repeated document in collection
                if post['selftext'] != "[removed]" and post['selftext'] != '[deleted]':
                    post_selftext = cleaning(post['selftext'])
                    post_title = cleaning(post['title'])
                    print("doing")
                    print(post['utc_datetime_str'])
                    name_count = name_counter(post_selftext)
                    post_document = {'id': post['id'], 
                                'utc_datetime_str' : post['utc_datetime_str'],
                                'created_utc' : post['created_utc'], 
                                'title': post_title,
                                'score': post['score'],
                                'selftext': post_selftext,
                                'link_flair_text': post['link_flair_text'],
                                'stocks_mentioned': name_count[0],
                                'mentioned_num': name_count[1],
                                'sentiment': sentiment_measure(post_title, post_selftext)}
                    post_collection.update_one({"id": post_document['id']}, {"$set": post_document}, upsert=True)
            print("stop")
            # recurse until there is no more post to add to collection 
            if posts['data'] and end_time_input != latest_time_doc:
                latest_time_doc = end_time_input
                end_time_input = post_collection.find_one({}, sort=[('created_utc', 1)])["created_utc"]
                print(end_time_input)
                print(latest_time_doc)
            # delete old documents(older than two years) for data storage efficiency
            else:
                if post_collection.find({"created_utc": { "$lte" : two_years_from_today_epoch} }):
                    post_collection.delete_many({"created_utc" : { "$lte" : two_years_from_today_epoch} })
                print("end")
                break
        except socket.timeout:
            # when timeout, it just passes and try again 
            pass
    return 

def post_data_analyzer(start_time, end_time):
    # set a dataframe for reddit post data within the range of data inputted and return the dataframe
    post_df = pd.DataFrame(list(post_collection.find({"created_utc": {"$lte": end_time, "$gte": start_time}})))
    print(post_df)
    pos_count, neg_count = 0, 0    
    company_count = company_name_dict.copy()
    for index, row in post_df.iterrows():
        pos_count += row['sentiment'][0]
        neg_count += row['sentiment'][1]
        index = 0
        for num in row['mentioned_num']:
            if num != 0:
                company_count[row['stocks_mentioned'][index]] += num
                index += 1
            
    sentiment_ratio = round(pos_count/neg_count, 5)
    company_count = sorted(company_count.items(), key=lambda x: x[1], reverse=True)[:25]
    
    data_mentioned_stock = {
        'Name' : [company_capitalize_dict[val[0]] for val in company_count],
        'Ticker' : [company_ticker_dict[val[0]].upper() for val in company_count],
        'Mentioned' : [dict[1] for dict in company_count],
        'Highest' : [],
        'Lowest' : [],
        'Change vs Dow': [],
        'Change vs S&P500': [],
        'Change vs Nasdaq': []
    } 
    post_df = analyze_stock(data_mentioned_stock, start_time, end_time)
    print(post_df)
    return [post_df, sentiment_ratio]

# def name_counter(df):
#     # Count ticker or company names mentioned in each post(a post can mention the same company name multple times, so one count per post)
#     for text in df['selftext']:
#         for word in word_tokenize(text):
#             if word in list(ticker_name_dict.keys()):
#                 ticker_name_dict[word] += 1
#             elif word in list(company_name_dict.keys()):
#                 company_name_dict[word] += 1
            
#     # sums up the number of times a company is mentioned by name and ticker
#     company_mentioned_together = company_name_dict.copy()
#     for key, value in company_ticker_dict.items():
#         company_mentioned_together[key] += ticker_name_dict[value]
#     company_mentioned_together = {key: value for key, value in sorted(company_mentioned_together.items(), key=lambda item: item[1], reverse=True)}    

#     name_list, ticker_list, mentioned_num = [], [], []

#     for key, value in company_mentioned_together.items():
#         name_list.append(company_capitalize_dict[key])
#         ticker_list.append(ticker_capitalize_dict[company_ticker_dict[key]])
#         mentioned_num.append(value)

#     # rank top 25 most mentioned stops
#     data_mentioned_stock = {
#         'Name' : name_list[:25],
#         'Ticker' : ticker_list[:25],
#         'Mentioned' : mentioned_num[:25],
#         'Highest' : [],
#         'Lowest' : [],
#         'Change vs S&P500': [],
#     } 
#     return data_mentioned_stock
