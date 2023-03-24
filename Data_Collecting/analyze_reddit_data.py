from reddit_posts_data_generator import data_mentioned_stock, date_range, post_data
import yfinance as yf
import pandas as pd 
import yahooquery 
from collections import Counter

# Generates useful finanical data for the mentioned stocks list  
def financial_data_generator(ticker):
    data = pd.DataFrame(data=yf.Ticker(ticker).history(start=date_range[0], end=date_range[1]))
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date
    data.set_index('Date', inplace=True)
    del data['Stock Splits'], data['Dividends']
    data[['Open', 'High', 'Low', 'Close']] = round(data[['Open', 'High', 'Low', 'Close']], 2)
    return data

# Used data of 'SPY' ETF (S&P 500 index fund)  
sp500_data = financial_data_generator('SPY')
sp500_return = ((sp500_data['Close'][-1] - sp500_data['Close'][0])/sp500_data['Close'][0]) * 100

# Add historical information for the mentioned stocks to data_mentioned_stock
for tcker in data_mentioned_stock['Ticker']:
    stock_financial_data = financial_data_generator(tcker)
    data_mentioned_stock['Highest'].append(max(stock_financial_data['High']))
    data_mentioned_stock['Lowest'].append(min(stock_financial_data['Low']))
    stock_return_num = ((stock_financial_data['Close'][-1] - stock_financial_data['Close'][0]
                                                                     )/stock_financial_data['Close'][0]) * 100
    data_mentioned_stock['Change vs S&P500'].append(str(round(((100 + stock_return_num)/(100 + sp500_return) - 1)*100, 2))+'%')

# convert to dataframe to make it more readable, index starting from 1 
data_mentioned_stock = pd.DataFrame(data=data_mentioned_stock, 
                                               index=pd.RangeIndex(start=1, stop=26))
# Import negative, positive word files and convert it to a list 
neg_word_list = open('Data/sentiment_wordslist/negative_words.txt', 'r').read().splitlines()
pos_word_list = open('Data/sentiment_wordslist/positive_words.txt', 'r').read().splitlines()

# make variables to count negative, positive terms mentioned in selftext
neg_word_count, pos_word_count = [], []

# Count negative, positive words used and return the result and ratio
def sentiment_measure():
    # global neg_word_count, pos_word_count
    # for title in post_data['title']:
    #     for title_word in title.split():
    #         if title_word in neg_word_list:
    #             neg_word_count.append(title_word)
    #         elif title_word in pos_word_list:
    #             pos_word_count.append(title_word)
    # for text in post_data['selftext']:
    #     for text_word in text.split():
    #         if text_word in neg_word_list:
    #             neg_word_count.append(text_word)
    #         elif text_word in pos_word_list:
    #             pos_word_count.append(text_word)
    # counter_neg = Counter(neg_word_count)
    # counter_pos = Counter(pos_word_count)
    # print(counter_neg)
    # print(counter_pos)
    global neg_word_count, pos_word_count
    for title in post_data['title']:
        for title_word in title.split():
            if title_word in neg_word_list:
                neg_word_count += 1
            elif title_word in pos_word_list:
                pos_word_count += 1
    for text in post_data['selftext']:
        for text_word in text.split():
            if text_word in neg_word_list:
                neg_word_count += 1
            elif text_word in pos_word_list:
                pos_word_count += 1
    print(f'Positive terms: count {pos_word_count}, Negative terms count: {neg_word_count}')
    return round(pos_word_count/neg_word_count, 5)

sentiment_measure()

