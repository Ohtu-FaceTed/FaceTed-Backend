from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src import db


class Session(db.Model):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    session_ident = Column(String(128), nullable=False)
    buildclass_id = Column(Integer, ForeignKey(
        "building_class.id"), nullable=True)
    selected_class = relationship("building_class")
    answered_questions = relationship(
        "answer_question", back_populates="session")

    def __repr__(self):
        return f"<Answer(session_ident='{self.sessionIdent}')>"

    def __init__(self, sess):
        self.session_ident = sess
