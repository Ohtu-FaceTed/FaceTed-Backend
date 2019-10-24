from sqlalchemy import Column, Integer, String
<<<<<<< HEAD
<<<<<<< HEAD
from src import db

=======
from . import db
>>>>>>> Added BuildingClass and Attribute SQL models, Changed SQL models to match
=======
from src import db
>>>>>>> Models for Session and QuestionAnswer

class Attribute(db.Model):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(String(12), nullable=False)
    attribute_name = Column(String(64), nullable=False)
<<<<<<< HEAD
    attribute_question = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<Attribute(attribute_id='{self.attribute_id}', attribute_name='{self.attribute_name}', attribute_question='{self.attribute_question}')>"
=======
    attribute_question = Column(String(64), nullable= False)

    def __repr__(self):
        return f"<Attribute(attribute_id='{self.attribute_id}', attribute_name='{self.attribute_name}', attribute_question='{self.attribute_question}')>"
>>>>>>> Added BuildingClass and Attribute SQL models, Changed SQL models to match
