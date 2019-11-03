from flask import Blueprint

views = Blueprint('views', __name__)


def init_app(app):
    with app.app_context():
        # Register routes with the app
        from . import answer
        from . import index
        from . import previous
        from . import question
        from . import feedback

        # Register blueprint
        app.register_blueprint(views)
