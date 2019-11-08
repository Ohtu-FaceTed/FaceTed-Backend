from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

#csrf = CSRFProtect()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    #csrf.init_app(app)

    # prints for debugging
    #app.config["SQLALCHEMY_ECHO"] = True

    # load production secret key
    app.config.from_pyfile('../secret_key.py')

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
