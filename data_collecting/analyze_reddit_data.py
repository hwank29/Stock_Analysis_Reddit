import yfinance as yf
import pandas as pd 
import datetime as dt
# Generates useful finanical data for the mentioned stocks list  
def financial_data_generator(ticker, start_date, end_date):
    data = pd.DataFrame(data=yf.Ticker(ticker).history(start=start_date, end=end_date))
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date
    data.set_index('Date', inplace=True)
    del data['Stock Splits'], data['Dividends'], data['Open']
    data[['High', 'Low', 'Close']] = round(data[['High', 'Low', 'Close']], 2)
    return data

def analyze_stock(post_df, start_date, end_date):
    # Used data of S&P 500 index fund
    sp500_data = financial_data_generator('^GSPC', start_date, end_date)
    sp500_return = ((sp500_data['Close'][-1] - sp500_data['Close'][0])/sp500_data['Close'][0]) * 100
    # Used data of Dow index fund
    dow_data = financial_data_generator('^DJI', start_date, end_date)
    dow_return = ((dow_data['Close'][-1] - dow_data['Close'][0])/dow_data['Close'][0]) * 100
    # Used data of Nasdaq index fund
    nasdaq_data = financial_data_generator('^IXIC', start_date, end_date)
    nasdaq_return = ((nasdaq_data['Close'][-1] - nasdaq_data['Close'][0])/nasdaq_data['Close'][0]) * 100    

    # Add historical information for the mentioned stocks to data_mentioned_stock
    for tcker in post_df['Ticker']:
        stock_financial_data = financial_data_generator(tcker, start_date, end_date)
        post_df['Highest'].append(max(stock_financial_data['High']))
        post_df['Lowest'].append(min(stock_financial_data['Low']))
        stock_return_num = ((stock_financial_data['Close'][-1] - stock_financial_data['Close'][0]
                                                                        )/stock_financial_data['Close'][0]) * 100
        post_df['Change vs Dow'].append(str(round(((100 + stock_return_num)/(100 + dow_return) - 1)*100, 2))+'%')
        post_df['Change vs S&P500'].append(str(round(((100 + stock_return_num)/(100 + sp500_return) - 1)*100, 2))+'%')
        post_df['Change vs Nasdaq'].append(str(round(((100 + stock_return_num)/(100 + nasdaq_return) - 1)*100, 2))+'%')

    # convert to dataframe to make it more readable, index starting from 1 
    post_df = pd.DataFrame(data=post_df, index=pd.RangeIndex(start=1, stop=21))
    return post_df

# Import negative, positive word files and convert it to a list 
neg_word_list = open('data/sentiment_wordslist/negative_words.txt', 'r').read().splitlines()
pos_word_list = open('data/sentiment_wordslist/positive_words.txt', 'r').read().splitlines()

# make variables to count negative, positive terms mentioned in selftext
neg_word_count, pos_word_count = 0, 0
# Count negative, positive words used and return the result and ratio
def sentiment_measure(title, selftext):
    """ Code to find out which positive and negative words are most repeated"""
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
    # counts how many times negative and positive words are mentioned in the gathered title and selftext
    neg_word_count, pos_word_count = 0, 0
    for title_word in title.split():
        if title_word in neg_word_list:
            neg_word_count += 1
        elif title_word in pos_word_list:
            pos_word_count += 1
    for text_word in selftext.split():
        if text_word in neg_word_list:
            neg_word_count += 1
        elif text_word in pos_word_list:
            pos_word_count += 1
    print(f'Positive terms: count {pos_word_count}, Negative terms count: {neg_word_count}')
    return [pos_word_count, neg_word_count]

