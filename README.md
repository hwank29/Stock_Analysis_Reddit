# Stock Sentiment Analysis with Reddit 

## I. Introduction

There has been a gigantic inflow of retail investors after the outbreak of COVID-19 pandemic and FED continuing dovish policies. The market continued a massive bull rally, and stocks gained as if they would never come back. The public's interest in stocks skyrocketed, which led r/stocks, a financial subreddit, gain over 11x times its subscribers before the pandemic(460k in Jan 2020, 5.1M in Jan 2023). Active discussion and company analysis happen in the giant financial community. 

This project aims to help retail investors including myself :\), interested in knowing perspective of many retail investors, by process and filter out the subreddit's posts data and provide multiple useful index including top 25 most mentioned stocks and its performance compared 3 majors US index(Dow, S&P 500, Nasdaq), subreddit sentiment analysis following concepts of CNN's fear and greed index, and filtered high quality research and analysis posts.

## II. Data Collecting and Methods

### API 
I initially used Pushshift API to extract posts data from r/stocks. However, on May 2nd, 2023, developers of the API decided to shut it down. So I had to restructure all my code from using Pushshift API to praw API. Using praw, I extracted each post's title, selftext, created_utc, link_flair_text, url, score.

Also, I used yfinance API to to gather in-depth financial data including daily highest, lowest, closed price, and performance compared to 3 majors index. 

### Data Filtering/Processing
After receiving post data from praw, I applied 'cleaning' function on selftext and title, which used regular expression to filter out stopwords downloaded from NLTK python package, hyperlinks, and unnecessarily repeated words. This is done to reduce time complexity. Then, I tokenized the filtered selftext and counted stocks names or tickers and their mentioned number and used pandas to organize and analyze the data. 

<p float="left">
  <img src="readme_images/cleaning.png" width="100" />
  <img src="readme_images/name_counter.png" width="100" /> 
</p>

### Database 
I used MongoDB to store the processed post data. All the documents are within 2 years, and they are updated with celery. Under 'posts_database', there are 2 collections: 'post_collection', with fields of _id, created_utc, mentioned_num, sentiment, stocks_mentioned and 'post_rank_collection', with fields of _id, link_flair_text, score, created_utc, url, title. Under 'post_collection', there are over 25,000 documents, 2 years worth of filtered post data. Under 'post_rank_collection', there are around 700 documents, high quality filtered posts in recent 2 years.  

### Background task
The data updating process is done as a background task through celery, which use redis as backend and broker. It asynchronously does the task to give most up to date accurate data for users. By using celery beat, it is scheduled to do data collecting process every 4 hours.

<img src="readme_images/celery_screenshot.png" width="50" />

## III. Analysis


## IV. Docker and AWS

## V. Result and Self-reflection and suggestions

## VI. Conclusion

## Conclusion and my thoughts

## Contributors
Hwanhee Kim(voiucee@gmail.com)

## Citation
Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
    Proceedings of the ACM SIGKDD International Conference on Knowledge 
    Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
    Washington, USA, 

