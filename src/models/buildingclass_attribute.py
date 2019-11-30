from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime, func, Float, Boolean
from sqlalchemy.orm import relationship
from . import db


class ClassAttribute(db.Model):
    __tablename__ = 'class_attribute'

    id = Column(Integer, primary_key=True)
    custom_probability = Column(Float, nullable=True)
    class_has_attribute = Column(Boolean, nullable=False)
    
    attribute_id = Column(Integer, ForeignKey('attribute.id'))
    buildingclass_id = Column(Integer, ForeignKey('building_class.id'))
    attribute = relationship("Attribute")
    answer = relationship("BuildingClass")


    def __init__(self, attribute, answer, session):
        self.attribute_id = attribute.id
        self.answer_id = answer.id
        self.session_id = session.id

    def __repr__(self):
        return f"<AnswerQuestion(attribute_id='{self.attribute_id}', answer_id='{self.answer_id}')>"
