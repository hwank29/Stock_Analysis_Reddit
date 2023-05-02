from data_collecting.reddit_posts_data_generator import post_data_analyzer, two_years_from_today_epoch, today_epoch
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
        if epoch_start_date < epoch_end_date and epoch_end_date < today_epoch and epoch_end_date > two_years_from_today_epoch:
            # if the database is empty or the latest date in any collection is later than the end date, go through data_collecting.reddit_posts_data_generator.py  
            return redirect(url_for('result', epoch_start_date=epoch_start_date, epoch_end_date=epoch_end_date))
        flash('* Incorrect Input Format! *')
    # my_task.delay()
    return render_template('main.html')

@app.route('/result/start=<epoch_start_date>/end=<epoch_end_date>')
def result(epoch_start_date, epoch_end_date):
    print(epoch_start_date, epoch_end_date)
    post_df = post_data_analyzer(epoch_start_date, epoch_end_date)
    print(post_df)
    return render_template("result.html", column_names=post_df[0].columns.values, row_data=list(post_df[0].values.tolist()), zip=zip, pos_neg_index=post_df[1], pos_count=post_df[2], neg_count=post_df[3])



            
