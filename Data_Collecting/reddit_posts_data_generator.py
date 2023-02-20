from urllib.request import urlopen
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import datetime as dt
import string
import json
import csv
import nltk
import os
import re
import csv
import requests 
import string

def date_conversion(time):
    # If the input was in YYYY-MM-DD format
    if re.search('^[\d]{4}-[\d]{2}-[\d]{2}$', time):
        date = dt.datetime.strptime(time, '%Y-%m-%d')
        #return timestamp
        return dt.datetime.timestamp(date)
    # if the input was in timestamp format if you have specific time 
    return time

# Converts YYYY-MM-DD to epoch time. 'before' and 'after' accept epoch for precise time
start_date_input = int(date_conversion(input("What would be your start time?(Format -- YYYY-MM-DD | timestamp(ex.1669824000)) :")))
end_date_input =  int(date_conversion(input("What would be your end time?(Format -- YYYY-MM-DD | timestamp(ex.1669824000)) :")))

# Organize company name and ticker dictionaries 
with open('Data/S&P500_tickers_names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    ticker_name_dict = {}
    company_name_dict = {}
    for company in csv_reader:
        ticker_name_dict[company['Ticker'].lower()] = 0
        company_name_dict[company['Name'].lower()] = 0 

# Data cleaning unneccessary parts of selftext 
def cleaning(text):    
    stop_words = set(stopwords.words('english'))
    # Makes a variable for stop words and remove any stop words from column title and selftext
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
    # Removes stop words(Ex. 'a', 'an', 'the', 'we')
    text = " ".join([t for t in text_tokenize if not t in stop_words])
    return text

# Function to generate data of posts in 'stocks' subreddit during the input time 
def post_data_generator(start_time, end_time):
    # Declare filtered_posts without initilizing
    filtered_posts = None
    # https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after=1609502400&before=1673352000&size=1000&is_video=false&fields=id,created_utc,title,score,upvote_ratio,selftext
    # Can pull 1000 reddit posts per request at max 
    post_data_generator_uri = f'https://api.pushshift.io/reddit/search/submission?subreddit=stocks&after={start_time}&before={end_time}&size=1000&is_video=false&fields=id,created_utc,utc_datetime_str,title,score,upvote_ratio,selftext'
    def get(uri):
        response = urlopen(uri)
        return json.loads(response.read())
    posts = get(post_data_generator_uri)
    first_time = True

    # Loops to store reddit post data 
    for post in posts['data']:
        if post['selftext'] != '[removed]' and post:
            value_input = {'id': post['id'], 
                           'utc_datetime_str' : post['utc_datetime_str'],
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
    try: 
        if posts['data']:
            filtered_posts = pd.concat([filtered_posts, post_data_generator(start_time, filtered_posts.iloc[-1]['created_utc'])], ignore_index = True)
    except:
        pass
    return filtered_posts

post_data = post_data_generator(start_date_input, end_date_input)
post_num = len(post_data)

# Count ticker or company names mentioned in each post(a post can mention the same company name multple times, so one count per post)
for text in post_data['selftext']:
    mentioned_list = []
    for word in word_tokenize(text):
        if word in list(ticker_name_dict.keys()):
            ticker_name_dict[word] += 1
            mentioned_list.append(word)
        elif word in  list(company_name_dict.keys()):
            company_name_dict[word] += 1
            mentioned_list.append(word)
print(list(ticker_name_dict.keys()))


print(sum(ticker_name_dict.values()))
print(sum(company_name_dict.values()))