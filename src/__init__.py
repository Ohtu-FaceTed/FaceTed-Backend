from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

# Global objects
from .naive_bayes_classifier import NaiveBayesClassifier
from .building_data import BuildingData
building_data = BuildingData()  # Overriden in create_app
classifier = NaiveBayesClassifier('./data/observations.csv')


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    csrf.init_app(app)

    # load production secret key
    app.config.from_pyfile('../secret_key.py')

    # Enable cross-origin request support
    CORS(app, supports_credentials=True)

    from . import views
    views.init_app(app)

    from . import models
    models.init_app(app)

    # Initialize the BuildingData cache object
    building_data.app = app
    building_data.load_from_db()

    return app
