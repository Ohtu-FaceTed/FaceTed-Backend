from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

csrf = CSRFProtect()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    csrf.init_app(app)

    # prints for debugging
    #app.config["SQLALCHEMY_ECHO"] = True

    # load production secret key
    app.config.from_pyfile('../secret_key.py')

    # Enable cross-origin request support
    CORS(app, supports_credentials=True)

    from . import models
    models.init_app(app)
        
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "views.auth_login"
    login_manager.login_message = "Please login to use this functionality."

    from .models.admin import Admin
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(user_id)

    from . import views
    views.init_app(app)

    return app


from .naive_bayes_classifier import NaiveBayesClassifier
from .building_data import BuildingData
# Default objects. These should be overriden by the app
building_data = BuildingData('')
classifier = NaiveBayesClassifier(building_data.observations)


