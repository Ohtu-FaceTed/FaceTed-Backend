from sqlalchemy import Column, Integer, String
<<<<<<< HEAD
from src import db

=======
from . import db
>>>>>>> Added BuildingClass and Attribute SQL models, Changed SQL models to match

class BuildingClass(db.Model):
    __tablename__ = 'building_class'

    id = Column(Integer, primary_key=True)
    class_id = Column(String(24), nullable=False)
    class_name = Column(String(64), nullable=False)

    def __repr__(self):
<<<<<<< HEAD
        return f"<BuildingClass(class_id='{self.class_id}', class_name='{self.class_name}')>"
=======
        return f"<BuildingClass(class_id='{self.class_id}', class_name='{self.class_name}')>"
>>>>>>> Added BuildingClass and Attribute SQL models, Changed SQL models to match
