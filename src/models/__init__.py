from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

    from .answer import Answer
    from .answer_question import AnswerQuestion
    from .attribute import Attribute
    from .building_class import BuildingClass
    from .session import Session

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print('Failed to create tables:', e)
