import argparse
import os
import pandas as pd

from sqlalchemy.exc import IntegrityError

from src import create_app
from src.models import db, Answer, Attribute, BuildingClass, QuestionGroup
from src.building_data import load_attributes, load_building_classes, load_attribute_groups
from config import ProductionConfig


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Import building data into database')
    parser.add_argument('data_directory', 
        help='Directory containing data CSV files')
    parser.add_argument('sql_file',
        help='SQLite target file')
    parser.add_argument('--verbose', action='store_true',
        help='Turn on SQL command echo')
    args = parser.parse_args()

    # Use a testing config for echoing database commands, but change the
    # database URI to the target file
    config = ProductionConfig()
    config.SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath(args.sql_file)}'
    config.SQLALCHEMY_ECHO = True if args.verbose else False

    # Create app to register database
    app = create_app(config)

    # load attributes groupings
    attribute_groups_path = os.path.join(args.data_directory, 'attribute_groups.csv')
    if os.path.isfile(attribute_groups_path):
        attribute_groups_df = load_attribute_groups(attribute_groups_path)
        
        with app.app_context():
            try:
                for i, x in attribute_groups_df.iterrows():
                    db.session.add(QuestionGroup(grouping_key=x.group_id,
                                                 group_name=x.group_name,
                                                 group_question=x.group_question))
                db.session.commit()
            except IntegrityError as e:
                print('Caught integrity error:', e.args[0])
                db.session.rollback()                
    else:
        print(f'Could not find attribute_groups.csv at: {attribute_groups_path}')


    # Load answer types
    with app.app_context():
        try:
            for x in ['yes', 'no', 'skip']:
                db.session.add(Answer(value=x))
            db.session.commit()
        except IntegrityError as e:
            print('Caught integrity error:', e.args[0])
            db.session.rollback()

    # Load attributes
    attribute_path = os.path.join(args.data_directory, 'attributes.csv')
    if os.path.isfile(attribute_path):
        attributes_df = load_attributes(attribute_path)
        
        with app.app_context():
            try:
                for i, x in attributes_df.iterrows():
                    db.session.add(Attribute(attribute_id=x.attribute_id,
                                             attribute_name=x.attribute_name,
                                             attribute_question=x.attribute_question,
                                             grouping_id=x.group_id,
                                             active=x.active,
                                             attribute_tooltip= x.attribute_tooltip))
                db.session.commit()
            except IntegrityError as e:
                print('Caught integrity error:', e.args[0])
                db.session.rollback()
                
        
    else:
        print(f'Could not find attribute.csv at: {attribute_path}')

    # Load classifications
    building_classes_path = os.path.join(args.data_directory, 'building_classes.csv')
    if os.path.isfile(building_classes_path):
        building_classes_df = load_building_classes(building_classes_path)
        
        with app.app_context():
            try:
                for i, x in building_classes_df.iterrows():
                    db.session.add(BuildingClass(class_id=x.class_id,
                                                class_name=x.class_name))
                db.session.commit()
            except IntegrityError as e:
                print('Caught integrity error:', e.args[0])
                db.session.rollback()
                
    else:
        print(f'Could not find building_classes.csv at: {building_classes_path}')

    
        
    
    