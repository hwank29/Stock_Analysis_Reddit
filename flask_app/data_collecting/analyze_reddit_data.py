import yfinance as yf
import pandas as pd 

# Generates useful finanical data for the mentioned stocks list  
def financial_data_generator(ticker, start_date, end_date):
    data = pd.DataFrame(data=yf.Ticker(ticker).history(start=start_date, end=end_date))
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.date
    data.set_index('Date', inplace=True)
    del data['Stock Splits'], data['Dividends'], data['Open']
    data[['High', 'Low', 'Close']] = round(data[['High', 'Low', 'Close']], 2)
    return data

# Analyze using yfinance
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
    index_change = ([round(dow_return, 2), dow_data['Close'][0], dow_data['Close'][-1]], [round(sp500_return, 2), sp500_data['Close'][0], sp500_data['Close'][-1]], [round(nasdaq_return, 2), nasdaq_data['Close'][0], nasdaq_data['Close'][-1]])
    # convert to dataframe to make it more readable, index with in total 25
    post_df = pd.DataFrame(data=post_df, index=pd.RangeIndex(start=1, stop=26))
    return [post_df, index_change]
