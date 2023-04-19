from website import app
from flask import render_template, request, flash, redirect
import datetime as dt 
from dateutil.relativedelta import relativedelta
from data_collecting.reddit_posts_data_generator import post_data_generator, three_years_from_today_epoch, today_epoch

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        start_date = dt.datetime.strptime(request.form.get("start"), '%Y-%m-%d')
        end_date = dt.datetime.strptime(request.form.get("end"), '%Y-%m-%d')
        epoch_start_date = int(dt.datetime.timestamp(start_date))
        epoch_end_date = int(dt.datetime.timestamp(end_date))

        # checks basic conditions for start and end date and if not met show an error
        if epoch_start_date < epoch_end_date and epoch_end_date < today_epoch and epoch_end_date > three_years_from_today_epoch:
           
            # if the database is empty or the latest date in any collection is later than the end date, go through data_collecting.reddit_posts_data_generator.py  
            post_df = post_data_generator(epoch_start_date, epoch_end_date)
            print(post_df)
            print(len(post_df.index))
            return f"Your start date is {dt.datetime.timestamp(start_date)} and your end date is {dt.datetime.timestamp(end_date)}"
        flash('* Incorrect Input Format! *')
    return render_template('main.html')
