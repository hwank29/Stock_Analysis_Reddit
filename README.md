# Stock Sentiment Analysis with Reddit 

## I. Introduction

There has been a gigantic inflow of retail investors after the outbreak of COVID-19 pandemic and FED continuing dovish policies. The market continued a massive bull rally, and stocks gained as if they would never come back. The public's interest in stocks skyrocketed, which led r/stocks, a financial subreddit, gain over 11x times its subscribers before the pandemic(460k in Jan 2020, 5.1M in Jan 2023). Active discussion and company analysis happen in the giant financial community. 

This project aims to help retail investors including myself :\), interested in knowing perspective of many retail investors, by process and filter out the subreddit's posts data and provide multiple useful index including top 25 most mentioned stocks and its performance compared 3 majors US index(Dow, S&P 500, Nasdaq), subreddit sentiment analysis following concepts of CNN's fear and greed index, and filtered high quality research and analysis posts.

## II. Data Collecting and Methods

### API 
I initially used Pushshift API to extract posts data from r/stocks. However, on May 2nd, 2023, developers of the API decided to shut it down. So I had to restructure all my code from using Pushshift API to praw API. Using praw, I extracted each post's title, selftext, created_utc, link_flair_text, url, score.

Also, I used yfinance API to to gather in-depth financial data including daily highest, lowest, closed price, and performance compared to 3 majors index. 

### Data Filtering/Processing
After receiving post data from praw, I tokenized selftext and title applied 'cleaning' function, which used regular expression to filter out stopwords downloaded from NLTK python package, hyperlinks, and unnecessarily repeated words. This is done to reduce capacity. Then, with the filtered selftext, I searched if a stock name or ticker is mentioned and count which stocks are mentioned their count numbers. I organized the data into stored it using MongoDB database. 

![cleaning function in reddit_posts_data_generator.py](read_shots/cleaning.png "cleaning function")

This data storing process is done as a background taks using celery. Celery workers asynchronously do the task to give most up to date accurate data for users. 2 years  


### Filtering

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

###

## Self-reflect and suggestions

## Conclusion

## Contributors
Hwanhee Kim(voiucee@gmail.com)

## Citation
Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
    Proceedings of the ACM SIGKDD International Conference on Knowledge 
    Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
    Washington, USA, 

