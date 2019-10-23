from .. import app

# SQLAlchemy import and setup
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# prints for debugging
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)



# create tables
try:
    db.create_all()
except:
    pass


#from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()