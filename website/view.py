from data_collecting.reddit_posts_data_generator import post_data_analyzer, two_years_from_today_epoch, today_epoch
from flask import render_template, request, flash, redirect
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
        my_task.delay()

        # checks basic conditions for start and end date and if not met show an error
        if epoch_start_date < epoch_end_date and epoch_end_date < today_epoch and epoch_end_date > two_years_from_today_epoch:
           
            # if the database is empty or the latest date in any collection is later than the end date, go through data_collecting.reddit_posts_data_generator.py  
            post_df = post_data_analyzer(epoch_start_date, epoch_end_date)
            return f"Your start date is {dt.datetime.timestamp(start_date)} and your end date is {dt.datetime.timestamp(end_date)}, and sentiment ratio is {post_df[1]}"
        flash('* Incorrect Input Format! *')
    return render_template('main.html')
