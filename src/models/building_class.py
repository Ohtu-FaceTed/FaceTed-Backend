from sqlalchemy import Column, Integer, String
from src import db


class BuildingClass(db.Model):
    __tablename__ = 'building_class'

    id = Column(Integer, primary_key=True)
    class_id = Column(String(24), nullable=False)
    class_name = Column(String(64), nullable=False)

    def __repr__(self):
        return f"<BuildingClass(class_id='{self.class_id}', class_name='{self.class_name}')>"
