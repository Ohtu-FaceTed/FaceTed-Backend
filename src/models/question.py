from sqlalchemy import Column, Integer, String
from . import Base

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(String(12), nullable=False)
    attribute_question = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<Question(attribute_id='{self.attribute_id}', attribute_question='{self.attribute_question}')>"
