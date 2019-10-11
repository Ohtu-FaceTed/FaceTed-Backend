import os
from flask import Flask, escape, request
app = Flask(__name__)

from src import question
from src import answer
from flask_cors import CORS
from os import urandom

app.config["SECRET_KEY"] = urandom(32)
# load actual secret key
app.config.from_pyfile('../config.py')
CORS(app, supports_credentials=True)

from .building_data import BuildingData
from .naive_bayes_classifier import NaiveBayesClassifier

# Default objects. These should be overriden by the app
building_data = BuildingData('', verbose=False)
classifier = NaiveBayesClassifier(building_data.observations)


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"