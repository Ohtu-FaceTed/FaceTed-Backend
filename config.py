class ProductionConfig():
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db'
    SQLALCHEMY_ECHO = False
    SECRET_KEY = '12345567890'  # Unsecure default
    WTF_CSRF_ENABLED = False


class TestingConfig():
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = '12345567890'  # Unsecure default
    WTF_CSRF_ENABLED = False
