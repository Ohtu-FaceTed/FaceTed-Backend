from sqlalchemy import Column, Integer, String
from src import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    value = Column(String(12), nullable=False)

    def __repr__(self):
        return f"<Answer(value='{self.value}')>"
