from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from . import db


class AnswerQuestion(db.Model):
    __tablename__ = 'answer_question'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    attribute_id = Column(Integer, ForeignKey('attribute.id'))
    answer_id = Column(Integer, ForeignKey('answer.id'))
    session_id = Column(Integer, ForeignKey('session.id'))

    attribute = relationship("Attribute")
    answer = relationship("Answer")

    session = relationship("Session", back_populates="answered_questions")

    def __init__(self, question, answer, session):
        self.question_id = question.id
        self.answer_id = answer.id
        self.session_id = answer.id

    def __repr__(self):
        return f"<AnswerQuestion(question_id='{self.question_id}', answer_id='{self.answer_id}')>"
