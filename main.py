
import csv 

#import  Data_Collecting/reddit_posts_data_generator.py 
import matplotlib.pyplot as plt

# Open csv file with S&P 500 ticker, company names and organize ticker and company names by putting them into the same list
with open('S&P500_tickers_names.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    ticker_company_name = []
    company_name_dict = {}
    ticker_name_together = [] #?
    for line in csv_reader:
        ticker_name_together.extend([line['Symbol'], line['Name']]) # Make a list that put
        ticker_company_name.append([line['Symbol'], line['Name']]) # Organize a list of ticker and company name
        company_name_dict[line['Name']] = 0 # Set company names to 0 in dictionary to show that they are not mentioned yet

# Counts how many posts were posted and put the data into bar chart
def count_posts_per_date(post_df, title, xlabel, ylabel):
    post_df.groupby([post_df.datetime.dt.date]).count().plot(y='id', rot=100, kind='bar', label='Posts')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.title('Weekly posts activity in r/stocks')
    plt.show()




# # Main function
# def main():
#     pass

# if __name__ == '__main__':
#     main()

# # """
# # BEGIN - DATAFRAME GENERATION FUNCTIONS

# # Here we are going to make a request to through the API
# # to the selected subreddit and the results are going 
# # to be placed inside a pandas dataframe
# # """

# # """FOR POSTS"""
# # def data_prep_posts(subreddit, start_time, end_time, filters, limit):
# #     if(len(filters) == 0):
# #         filters = ['id', 'author', 'created_utc',
# #                    'domain', 'url',
# #                    'title', 'num_comments']                 #We set by default some columns that will be useful for data analysis

# #     posts = list(api.search_submissions(
# #         subreddit=subreddit,                                #We set the subreddit we want to audit
# #         after=start_time,                                   #Start date
# #         before=end_time,                                    #End date
# #         filter=filters,                                     #Column names we want to get from reddit
# #         limit=limit))                                       #Max number of posts we wanto to recieve

# #     return pd.DataFrame(posts)                              #Return dataframe for analysis


# # """FOR COMMENTS"""
# # def data_prep_comments(term, start_time, end_time, filters, limit):
# #     if (len(filters) == 0):
# #         filters = ['id', 'author', 'created_utc',
# #                    'body', 'permalink', 'subreddit']        #We set by default some columns that will be useful for data analysis

# #     comments = list(api.search_comments(
# #         q=term,                                             #We set the subreddit we want to audit
# #         after=start_time,                                   #Start date
# #         before=end_time,                                    #End date
# #         filter=filters,                                     #Column names we want to get from reddit
# #         limit=limit))                                       #Max number of comments we wanto to recieve
# #     return pd.DataFrame(comments)                           #Return dataframe for analysis

# # """
# # END - DATAFRAME GENERATION FUNCTIONS
# # """
