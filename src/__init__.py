import os
from flask import Flask, escape, request
app = Flask(__name__)

#SQLAlchemy import and setup
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://app.db"
#prints for debugging
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


from flask_cors import CORS
from src import answer
from src import question

app.config["SECRET_KEY"] = os.urandom(32)
# load actual secret key
app.config.from_pyfile('../config.py')
CORS(app, supports_credentials=True)

from .naive_bayes_classifier import NaiveBayesClassifier
from .building_data import BuildingData
# Default objects. These should be overriden by the app
building_data = BuildingData('', verbose=False)
classifier = NaiveBayesClassifier(building_data.observations)


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"


#create tables
try:
    db.create_all()
except:
    pass
