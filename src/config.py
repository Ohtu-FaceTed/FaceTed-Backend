class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db'
    SQLALCHEMY_ECHO = True
    SECRET_KEY = '12345567890'  # Unsecure default


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.db'
