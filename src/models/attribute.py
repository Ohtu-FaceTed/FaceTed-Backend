from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from . import db


class Attribute(db.Model):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(String(12), nullable=False, unique=True)
    attribute_name = Column(String(64), nullable=False)
    attribute_question = Column(String(1000), nullable=False)
    grouping_id = Column(Integer, ForeignKey(
        "question_group.id"), nullable=True)
    part_of_group = relationship("QuestionGroup")
    active = Column(Boolean, nullable=True)
    attribute_tooltip = Column(String(1000), nullable=True)
    probability = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Attribute(attribute_id='{self.attribute_id}', attribute_name='{self.attribute_name}', attribute_question='{self.attribute_question}')>"
