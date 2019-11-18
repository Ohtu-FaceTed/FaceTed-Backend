import argparse
import os
import pandas as pd
import json

from sqlalchemy.exc import IntegrityError

from src import create_app
from src.models import db, Answer, Attribute, BuildingClass, QuestionGroup, Admin
#from src.building_data import load_attributes, load_building_classes, load_attribute_groups
from config import ProductionConfig

# The attribute dataframe should have at least the following columns
#   attribute_id: numerical attribute identifier (string, unique)
#   attribute_name: common name for class (string)
#   attribute_question: question form of attribute (string)
#   group_id: identifier of attribute group to which attribute belongs to (string)
#   active: indicates if the attribute should be used (boolean)
#   attribute_tooltip: tooltip on mouse over for given attribute (string)
DEFAULT_ATTRIBUTES = pd.DataFrame({'attribute_id': ['1', '101', '102', '114', '116'],
                                   'attribute_name': ['Asunnot', 'Asuinhuone',
                                                      'Eteinen', 'WC', 'WC-pesuhuone'],
                                   'attribute_question': ['{"fi":"Onko rakennuksessa asunnot?", "sv":"[Svenska]Onko rakennuksessa asunnot?", "en":"[English]Onko rakennuksessa asunnot?"}',
                                                          '{"fi":"Onko rakennuksessa asuinhuone?", "sv":"[Svenska]Onko rakennuksessa asuinhuone?", "en":"[English]Onko rakennuksessa asuinhuone?"}',
                                                          '{"fi":"Onko rakennuksessa eteinen?", "sv":"[Svenska]Onko rakennuksessa eteinen?", "en":"[English]Onko rakennuksessa eteinen?"}',
                                                          '{"fi":"Onko rakennuksessa wc?", "sv":"[Svenska]Onko rakennuksessa wc?", "en":"[English]Onko rakennuksessa wc?"}',
                                                          '{"fi":"Onko rakennuksessa wc-pesuhuone?", "sv":"[Svenska]Onko rakennuksessa wc-pesuhuone?", "en":"[English]Onko rakennuksessa wc-pesuhuone?"}'],
                                   'group_id': [None, None, None, '1', '1'],
                                   'active': [True, True, True, True, True],
                                   'attribute_tooltip': ['Onko rakennuksessa asunnot?',
                                                         'Onko rakennuksessa asuinhuone?',
                                                         'Onko rakennuksessa eteinen?',
                                                         'Onko rakennuksessa WC?',
                                                         'Onko rakennuksessa WC-pesuhuone?']},)


def load_attributes(attribute_file):
    '''Attempts to load attribute data from file into Pandas dataframe'''
    df = pd.read_csv(attribute_file, dtype=str)

    # Check that the required fields are present
    for required_field in ['attribute_id', 'attribute_name', 'attribute_question', 'group_id', 'active', 'attribute_tooltip']:
        if required_field not in df:
            raise ValueError(
                f"The attribute data ({attribute_file}) does not contain a '{required_field}' column!")
    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The attribute data ({attribute_file}) does not contain any rows!")
    # Change active column type to boolean
    df.active = df.active.astype(bool)

    # Ensure columns are imported as strings
    df.columns = df.columns.astype(str)
    return df

# The building classes dataframe should have at least the following fields:
#   class_id: four digit class identifier (string, unique)
#   class_name: common name for class (string)
DEFAULT_BUILDING_CLASSES = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                         'class_name': ['Omakotitalot',
                                                        'Paritalot',
                                                        'Rivitalot']})


def load_building_classes(building_classes_file):
    '''Attempts to load buiding class data from file into Pandas dataframe'''
    df = pd.read_csv(building_classes_file, dtype=str)

    # Check that the required fields are present
    for required_field in ['class_id', 'class_name']:
        if required_field not in df:
            raise ValueError(
                f"The building classes data ({building_classes_file}) does not contain a '{required_field}' column!")

    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The building classes data ({building_classes_file}) does not contain any rows!")

    # Ensure columns are imported as strings
    df.columns = df.columns.astype(str)

    return df

# The attribute groups dataframe should have at least the following columns:
#   group_id: attribute group identifier (string, unique)
#   group_name: common name for all group members (string)
#   group_question: question form of attribute group (string)
DEFAULT_ATTRIBUTE_GROUPS = pd.DataFrame({'group_id': ['1'],
                                         'group_name': ['WC:t'],
                                         'group_question': ['Minkälaisia WC-tiloja rakennuksessa on?']})


def load_attribute_groups(attribute_groups_file):
    '''Attempts to load attribute groups data from file into Pandas dataframe'''
    df = pd.read_csv(attribute_groups_file, dtype=str)

    # Check that the required fields are present
    for required_field in ['group_id', 'group_name', 'group_question']:
        if required_field not in df:
            raise ValueError(
                f"The attribute groups data ({attribute_groups_file}) does not contain a '{required_field}' column!")

    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The attribute groups data ({attribute_groups_file}) does not contain any rows!")

    # Ensure columns are imported as strings
    df.columns = df.columns.astype(str)

    return df


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

    # adds default user to db
    with app.app_context():
        if len(Admin.query.all()) == 0:
            with open('data/user.json') as f:
                data = json.load(f)
                db.session.add(Admin(data['name'],data['username'],data['password']))
                db.session.commit()

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

    
        
    
    