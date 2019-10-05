import os
from flask import Flask
app = Flask(__name__)   

from src import question
from src import answer
from flask_cors import CORS
from os import urandom
app.config["SECRET_KEY"] = urandom(32)


app.secret_key = 'dev'
# load actual secret key
app.config.from_pyfile('../config.py')
CORS(app, supports_credentials=True)


