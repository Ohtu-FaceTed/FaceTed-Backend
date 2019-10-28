import os
from flask import Flask, escape, request
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://app.db"
# prints for debugging
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.urandom(32)
# load actual secret key
app.config.from_pyfile('../config.py')

from flask_cors import CORS
CORS(app, supports_credentials=True)

from . import views
views.init_app(app)

from . import models
models.init_app(app)

from .naive_bayes_classifier import NaiveBayesClassifier
from .building_data import BuildingData
# Default objects. These should be overriden by the app
building_data = BuildingData('')
classifier = NaiveBayesClassifier(building_data.observations)




# create tables
try:
    db.create_all()
except:
    pass
