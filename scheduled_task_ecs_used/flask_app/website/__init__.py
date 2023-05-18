from flask import Flask, render_template, request
from pathlib import Path
import os 

# dotenv_path = Path('.env')
# load_dotenv(dotenv_path=dotenv_path)
# creates a flask app
secret_key = os.environ.get('secret_key')
app = Flask(__name__, static_folder="./static", template_folder="./templates")
app.config['SECRET_KEY'] = secret_key
# os.getenv("secret_key")

from . import view  