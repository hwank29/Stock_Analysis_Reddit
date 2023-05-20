from . import app
from flask import render_template, request, flash, redirect, url_for
# from celery_work.celery import my_task
import datetime as dt 
import sys
sys.path.append("..")
from data_collecting.reddit_posts_data_generator import post_data_analyzer, two_years_from_today_epoch, today_epoch, post_rank_collection

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        start_date = dt.datetime.strptime(request.form.get("start"), '%Y-%m-%d') #utc but today_epoch, two_year is not 
        end_date = dt.datetime.strptime(request.form.get("end"), '%Y-%m-%d') #utc
        epoch_start_date = start_date.replace(tzinfo=dt.timezone.utc).timestamp()
        # as epoch_end_date will return 12am of the day, all posts on that date would not be included to prevent added 86400(equivalent to 1 day)
        epoch_end_date = end_date.replace(tzinfo=dt.timezone.utc).timestamp() 
        # checks basic conditions for start and end date and if not met show an error
        if epoch_start_date < epoch_end_date and epoch_end_date < today_epoch and epoch_start_date + 86400 > two_years_from_today_epoch:
            return redirect(url_for("result", start=epoch_start_date, end=epoch_end_date))
        flash('* Incorrect Input Format! *')
    return render_template('main.html')

@app.route('/result?start=<start>&end=<end>')
def result(start, end):
    start, end = int(float(start)), int(float(end))
    post_df = post_data_analyzer(start, end)
    industry_discussion_list = list(post_rank_collection.find({"link_flair_text": "Industry Discussion", "created_utc": {"$gte": start, "$lte": end}}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
    company_discussion_list = list(post_rank_collection.find({"link_flair_text": "Company Discussion", "created_utc": {"$gte": start, "$lte": end}}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
    company_analysis_list = list(post_rank_collection.find({"link_flair_text": "Company Analysis", "created_utc": {"$gte": start, "$lte": end}}, {"_id": 0, "title": 1, "url": 1, "score": 1}).sort("score", -1).limit(15))
    
    return render_template("result.html", industry_discussion_list=industry_discussion_list, company_discussion_list=company_discussion_list, company_analysis_list=company_analysis_list,
                                            column_names= post_df[0].columns.values, row_data=list(post_df[0].values.tolist()), sentiment_index=post_df[1], pos_count=post_df[2], neg_count=post_df[3],
                                            index_change=post_df[4])



