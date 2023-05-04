from data_collecting.reddit_posts_data_generator import post_data_analyzer, two_years_from_today_epoch, today_epoch, post_rank_collection
from flask import render_template, request, flash, redirect, url_for
from website.tasks import my_task
from website import app
import datetime as dt 


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        start_date = dt.datetime.strptime(request.form.get("start"), '%Y-%m-%d')
        end_date = dt.datetime.strptime(request.form.get("end"), '%Y-%m-%d')
        epoch_start_date = int(start_date.replace(tzinfo=dt.timezone.utc).timestamp())
        epoch_end_date = int(end_date.replace(tzinfo=dt.timezone.utc).timestamp())
        # checks basic conditions for start and end date and if not met show an error
        if epoch_start_date < epoch_end_date and epoch_end_date < today_epoch and epoch_start_date > two_years_from_today_epoch:
            post_df = post_data_analyzer(epoch_start_date, epoch_end_date)
            industry_discussion_list = list(post_rank_collection.find({"link_flair_text": "Industry Discussion"}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
            company_discussion_list = list(post_rank_collection.find({"link_flair_text": "Company Discussion"}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
            company_analysis_list = list(post_rank_collection.find({"link_flair_text": "Company Analysis"}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
            
            return render_template("result.html", industry_discussion_list= industry_discussion_list, company_discussion_list=company_discussion_list, company_analysis_list=company_analysis_list,
                                                  column_names= post_df[0].columns.values, row_data=list(post_df[0].values.tolist()), sentiment_index=post_df[1], pos_count=post_df[2], neg_count=post_df[3],
                                                  index_change=post_df[4])
            # if the database is empty or the latest date in any collection is later than the end date, go through data_collecting.reddit_posts_data_generator.py  
            # return redirect(url_for('result', epoch_start_date=epoch_start_date, epoch_end_date=epoch_end_date))
        flash('* Incorrect Input Format! *')
    my_task.delay()
    return render_template('main.html')



