import os
from flask import Flask
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    #app.config["SQLALCHEMY_DATABASE_URI"] = 
    # prints for debugging
    #app.config["SQLALCHEMY_ECHO"] = True
    #app.config["SECRET_KEY"] = os.urandom(32)
    # load actual secret key
    #app.config.from_pyfile('../config.py')

    # Enable cross-origin request support
    CORS(app, supports_credentials=True)

    from . import views
    views.init_app(app)

    from . import models
    models.init_app(app)

    return app


from .naive_bayes_classifier import NaiveBayesClassifier
from .building_data import BuildingData
# Default objects. These should be overriden by the app
building_data = BuildingData('')
classifier = NaiveBayesClassifier(building_data.observations)
