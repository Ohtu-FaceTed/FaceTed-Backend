from sqlalchemy import Column, Integer, String
from src import db


class QuestionGroup(db.Model):
    __tablename__ = 'question_group'

    id = Column(Integer, primary_key=True)
    grouping_key = Column(String(24), nullable=False)

    def __repr__(self):
        return f"<QuestionGroup(grouping_key='{self.grouping_key}')>"
