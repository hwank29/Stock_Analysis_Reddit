from urllib.request import urlopen
from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt
import json
import os
import re
import csv
import requests 
import string
import nltk 
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Create an object of Pushshift API
api = PushshiftAPI()

# Creates a variable containing dataframe of S&P 500 stock tickers and names 
stock_names_df = pd.read_csv('Data/S&P500_tickers_names.csv')


# Converts YYYY-MM-DD to epoch time. 'before' and 'after' accept epoch for precise time
""" Need to be changed to input"""
start_date_input = int(dt.datetime(2022,11,1).timestamp())  
end_date_input = int(dt.datetime(2023,2,10).timestamp())  

# Open csv file with S&P 500 ticker, company names and organize ticker and company names by putting them into the same list
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
    stop_words = stopwords.words('english')    
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


filtered_posts = []
post_num = 0
# Function to generate data of posts in 'stocks' subreddit during the input time 
"""Somehow prints out the same results multiple times """
def post_data_generator(start_time=start_date_input, end_time=end_date_input):
    global filtered_posts
    # https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
    post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_time}&before={end_time}&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext'
    def get(uri):
        response = urlopen(uri)
        return json.loads(response.read())
    post_data = get(post_data_generator_uri)
    for post in post_data['data']:
        if post['selftext'] != '[removed]' and post:
            print('Hi')
            filtered_posts.append({'id': post['id'], 
                                   'created_utc' : post['created_utc'], 
                                   'title': cleaning(post['title']),
                                   'score': post['score'],
                                   'upvote_ratio': post['upvote_ratio'],
                                   'selftext': cleaning(post['selftext'])})        
    # Recurse until start_timek
    if start_time < filtered_posts[-1]['created_utc']: 
        print([filtered_posts[-1]['created_utc'], start_time])
        post_data_generator(start_time, filtered_posts[-1]['created_utc'])
        post_num += len(post_data['data'])
        print('Bye')
    return [filtered_posts, post_num]

print(post_data_generator())



# # Applies 'cleaning' function to a copy of post_data 
# filtered_post_data = post_data().apply(cleaning)

# # Makes a variable for stop words and remove any stop words from column title and selftext

# # Filters unnecessary stop words(ex. the, a, an, and) from title and selftext of filtered_post_data
# filtered_post_data['title'] = filtered_post_data['title'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
# filtered_post_data['selftext'] = filtered_post_data['selftext'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# # Export filtered data to a csv file and save it to Data folder 
# filtered_post_data.to_csv('Data/post_data.csv', index=False)
