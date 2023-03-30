from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv()

def create_app():

    # creates a flask app
    app = Flask(__name__, static_folder="static")
    # set MongoDB Client with specific mongodb uri
    client = MongoClient(os.getenv("MONGODB_URI"))
    # set 'db' equal to 'flask_db' database from client cluster 
    db = client.flask_db
    # set 'stocks' equal to a collection of 'db' database
    stocks = db.stocks

    @app.route('/', methods=['GET', 'POST'])
    def main():
        if request.method == "GET":
            return render_template('main.html')
        
        if request.method == 'POST':
            start_date = request.form.get("start")
            end_date = request.form.get("end")
            if end_date != :
            
            return render_template('result.html', result=[start_date, end_date])
            return f"Your start date is {start_date} and your end date is {end_date}"
        

    return app 

if __name__ == '__main__':
    create_app().run(port=5001, debug=True)
