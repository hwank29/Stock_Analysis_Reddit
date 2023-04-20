from flask import Flask, render_template, request


# creates a flask app
app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'bf955895e881eedfdb46241b9a026a1852612fb1850227374473d14b2f9f4fce'

from website import view

    
