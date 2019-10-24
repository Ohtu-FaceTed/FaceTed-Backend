from sqlalchemy import Column, Integer, String
from src import db


class Attribute(db.Model):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(String(12), nullable=False)
    attribute_name = Column(String(64), nullable=False)
    attribute_question = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<Attribute(attribute_id='{self.attribute_id}', attribute_name='{self.attribute_name}', attribute_question='{self.attribute_question}')>"
