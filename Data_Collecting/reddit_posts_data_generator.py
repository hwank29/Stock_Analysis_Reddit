from urllib.request import urlopen
import pandas as pd
import datetime as dt
import json
import os
import re
import csv
import requests 
import string


# Converts YYYY-MM-DD to epoch time. 'before' and 'after' accept epoch for precise time
""" Need to be changed to input"""
start_date_input = int(dt.datetime(2022,12,1).timestamp())  
end_date_input = int(dt.datetime(2023,2,10).timestamp())  

# def date_conversion(time):
#     if time[]
#     return str(dt.datetime.fromtimestamp(int(time)).date())

# print(date_conversion())
# Organize company name and ticker dictionaries 
with open('Data/S&P500_tickers_names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    ticker_name_dict = {}
    company_name_dict = {}
    for line in csv_reader:
        ticker_name_dict[line['Ticker']] = 0
        company_name_dict[line['Name']] = 0 

# Data cleaning unneccessary parts of selftext 
def cleaning(text):    
    # Makes a variable for stop words and remove any stop words from column title and selftext
    text = text.lower()
    # removes http and www website url
    text = re.sub('http\w+|www\.\S+', "", text)
    # removes special characters
    text = re.sub('<.*?>+', "", text)
    # removes digits
    text = re.sub("\d+", "", text)
    # removes tap and white space
    text = re.sub("\s\s+", " ", text)
    # removes punctuation besides $ for ticker 
    text = text.translate(str.maketrans('', '', string.punctuation.replace('$','') + '’'))
    return text

# Function to generate data of posts in 'stocks' subreddit during the input time 
def post_data_generator(start_time=start_date_input, end_time=end_date_input):
    # Declare filtered_posts without initilizing
    filtered_posts = None
    # https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
    # Can pull 1000 reddit posts per request at max 
    post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_time}&before={end_time}&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext'
    def get(uri):
        print('l')
        response = urlopen(uri)
        return json.loads(response.read())
    posts = get(post_data_generator_uri)
    first_time = True
    # Loops to store reddit post data 
    for post in posts['data']:
        if post['selftext'] != '[removed]' and post:
            value_input = {'id': post['id'], 
                           'created_utc' : post['created_utc'], 
                           'title': cleaning(post['title']),
                           'score': post['score'],
                           'upvote_ratio': post['upvote_ratio'],
                           'selftext': cleaning(post['selftext'])}
            if not first_time:
                filtered_posts = pd.concat([filtered_posts, pd.DataFrame([value_input])], ignore_index = True)   
            else:
                # Need to set filtered_posts before pd.concat
                first_time = False
                filtered_posts = pd.DataFrame([value_input])
    # Recurse until there is no more posts between 'before' and 'after' time 
    if posts['data']:
        filtered_posts = pd.concat([filtered_posts, post_data_generator(start_time, filtered_posts.iloc[-1]['created_utc'])], ignore_index = True)
    return filtered_posts

post_data = post_data_generator()
post_num = len(post_data)

