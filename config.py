from src.config import Config

class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False
    #secret key used in production to be stored here
