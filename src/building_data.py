import os
import sys
import numpy as np
import pandas as pd

# The attribute dataframe should have at least the following columns
#   attribute_id: numerical attribute identifier (string, unique)
#   attribute_name: common name for class (string)
#   attribute_question: question form of attribute (string)
DEFAULT_ATTRIBUTES = pd.DataFrame({'attribute_id': ['1', '101', '102'],
                                   'attribute_name': ['Asunnot', 'Asuinhuone',
                                                      'Eteinen'],
                                   'attribute_question': ['Onko rakennuksessa asunnot?',
                                                          'Onko rakennuksessa asuinhuone?',
                                                          'Onko rakennuksessa eteinen?']})


def load_attributes(attribute_file):
    '''Attempts to load attribute data from file into Pandas dataframe'''
    df = pd.read_csv(attribute_file, dtype=str)

    # Check that the required fields are present
    for required_field in ['attribute_id', 'attribute_name', 'attribute_question']:
        if required_field not in df:
            raise ValueError(
                f"The attribute data ({attribute_file}) does not contain a '{required_field}' column!")

    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The attribute data ({attribute_file}) does not contain any rows!")

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


# The observations dataframe should have at least the following columns:
#   class_id: same as building_classes class_id (string, unique)
#   count: number of observations of this class (int, positive)
#   [attribute]: number of observations of this attribute for a given class_id (integer)
DEFAULT_OBSERVATIONS = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                     'count': [1, 1, 1],
                                     '1': [1, 1, 1],
                                     '101': [1, 0, 1],
                                     '102': [0, 1, 0]})


def load_observations(observation_file):
    '''Attempts to load buiding-attribute observation data from file into Pandas dataframe'''
    df = pd.read_csv(observation_file, dtype={'class_id': str})

    # Check that the required fields are present
    for required_field in ['class_id', 'count']:
        if required_field not in df:
            raise ValueError(
                f"The observations data ({observation_file}) does not contain a '{required_field}' column!")

    # Check that we have at least one "attribute" column in addition to
    # class_id and count
    if len(df.columns) < 3:
        raise ValueError(
            f"The observation data ({observation_file}) does not contain any attribute columns!")

    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The observation data ({observation_file}) does not contain any rows!")

    # Check counts are positive integers
    if not np.equal(np.mod(df['count'], 1), 0).all or (df['count'] < 1).any():
        raise ValueError(
            "Found 'count' values in observation data that are not positive integers")

    # Ensure that the column labels are interpreted as strings
    df.columns = df.columns.astype(str)

    return df


class BuildingData:
    def __init__(self, data_directory):
        '''Initializes a BuildingData object using the data files in data_directory'''
        # Construct full paths to data files given data_directory
        attribute_file = os.path.join(data_directory, 'attributes.csv')
        building_classes_file = os.path.join(
            data_directory, 'building_classes.csv')
        observation_file = os.path.join(data_directory, 'observations.csv')

        # Try to load the data
        try:
            self._attributes = load_attributes(attribute_file)
            self._building_classes = load_building_classes(
                building_classes_file)
            self.observations = load_observations(observation_file)
        # If we experience any error in loading, replace all the data with the
        # default values
        except Exception as e:
            print(
                f'Failed to read building data: {e.args[0]}', file=sys.stderr)
            print('Substituting placeholder data!', file=sys.stderr)
            self._attributes = DEFAULT_ATTRIBUTES
            self._building_classes = DEFAULT_BUILDING_CLASSES
            self.observations = DEFAULT_OBSERVATIONS

        # Pre-generate dictionaries for accessing attribute features and names
        # by atrribute_id
        self._attributes_dict = {
            attr_id: {'attribute_id': attr_id,
                      'attribute_name': attr_name,
                      'attribute_question': attr_question}
            for ind, (attr_id, attr_name, attr_question) in self._attributes.iterrows()}
        self._attributes_names_dict = {
            attr_id: attr_name
            for ind, (attr_id, attr_name, attr_question) in self._attributes.iterrows()}

        # Pre-generate dictionary for accesing building class names by class_id
        self._building_classes_dict = {class_id: class_name for ind,
                                       (class_id, class_name) in self._building_classes.iterrows()}

    @property
    def attribute(self):
        '''Returns the attribute_id to attribute fields dict mapping'''
        return self._attributes_dict

    @property
    def attribute_name(self):
        '''Returns the attribute_id-attribute_name mapping'''
        return self._attributes_names_dict

    @property
    def building_class_name(self):
        '''Returns the building class_id-class_name mapping'''
        return self._building_classes_dict
