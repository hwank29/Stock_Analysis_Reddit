from pmaw import PushshiftAPI
import pandas as pd
import datetime as dt
import re 
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
start = int(dt.datetime(2021,1,1).timestamp())  
end = int(dt.datetime(2023,1,10).timestamp())  

# Function to generate data of posts in 'stocks' subreddit during the input time 
def post_data(start_time=start, end_time=end):
    post_data_generator = api.search_submissions(subreddit = 'stocks', limit = None, filter = ['title', 'selftext'], 
                                                 before = end_time, after = start_time, mem_safe = True)
    # Filters out deleted posts and set the dataframe of the filtered posts data as a variable
    raw_data = pd.DataFrame([submission for submission in post_data_generator if submission['selftext'] != '[removed]']) 

    # Removes 'created_utc' column as it is not used  
    del raw_data['created_utc']
    return raw_data

# Data cleaning unneccessary parts of selftext of post data
def cleaning(text):        
    # converts a text input into lowercase and remove any links, punctuations, special characters, indents, etc
    text = text.str.lower()
    text.replace(to_replace = 'https?://\S+|www\.\S+', value = '', inplace = True, regex = True)
    text.replace(to_replace = '<.*?>+', value = '', inplace = True, regex = True)
    text.replace(to_replace = '[%s]' % re.escape(string.punctuation), value = '', inplace = True, regex = True)
    text.replace(to_replace = '\n', value = '', inplace = True, regex = True)
    text.replace(to_replace = '[’“”…]', value = '', inplace = True, regex = True)
    return text

# Applies 'cleaning' function to a copy of post_data 
filtered_post_data = post_data().apply(cleaning)
# Makes a variable for stop words and remove any stop words from column title and selftext
stop_words = stopwords.words('english')
# Filters unnecessary stop words(ex. the, a, an, and) from title and selftext of filtered_post_data
filtered_post_data['title'] = filtered_post_data['title'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
filtered_post_data['selftext'] = filtered_post_data['selftext'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))



# from collections import Counter
# p = Counter(" ".join(dt).split()).most_common(10)
# rslt = pd.DataFrame(p, columns=['Word', 'Frequency'])
#print(rslt)

# Create a variable for most frquently appeared words after data cleaning 

#most_used_words = pd.DataFrame(pd.Series(' '.join(filtered_selftext_post_data).split()).value_counts()).to_string()

#print(most_used_words)

#for word in most_used_words['Word']:
#    print(word)



