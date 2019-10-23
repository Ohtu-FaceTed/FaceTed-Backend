from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


def init_app(app):
    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print('Failed to create tables:', e)
