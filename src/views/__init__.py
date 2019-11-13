import json
from flask import Blueprint

views = Blueprint('views', __name__)

default_language = 'fi'
supported_languages = ['en', 'fi', 'se']


def init_app(app):
    with app.app_context():
        # Register routes with the app
        from . import answer
        from . import index
        from . import previous
        from . import question
        from . import feedback
        from . import adminView
        from . import feedback

        # Register blueprint
        app.register_blueprint(views)


def get_best_match_language(languages):
    for lang in languages.values():
        if lang in supported_languages:
            return lang
    return default_language


def select_question_by_language(questionJson, language):
    question = json.loads(questionJson)

    if language is not None:
        if language in supported_languages:
            return question[language]
        else:
            print('language ' + language +
                  ' not supported for attribute : ' + questionJson)
            return question[default_language]
    else:
        print('language not defined')
        return question[default_language]
