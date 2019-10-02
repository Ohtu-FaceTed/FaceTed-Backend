import os
import sys
import pandas as pd

# The attribute dataframe should have at least the following columns
#   attribute_id: numerical attribute identifier (string, unique)
#   attribute_name: common name for class (string)
DEFAULT_ATTRIBUTES = pd.DataFrame({'attribute_id': ['1', '101', '102'], 
                                   'attribute_name': ['Asunnot', 'Asuinhuone', 
                                                      'Eteinen']})


def load_attributes(attribute_file):
    '''Attempts to load attribute data from file into Pandas dataframe'''
    try:
        df = pd.read_csv(attribute_file, dtype=str)

        # Check that the required fields are present
        assert 'attribute_id' in df
        assert 'attribute_name' in df
    except:
        print(f'Failed to load attribute data from {attribute_file}!', 
              file=sys.stderr)
        # If reading the data failed, use placeholder data, so some 
        # functionality is maintained
        df = DEFAULT_ATTRIBUTES

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
    try:
        df = pd.read_csv(building_classes_file, dtype=str)
        
        # Check that the required fields are present
        assert 'class_id' in df
        assert 'class_name' in df
    except:
        print(f'Failed to load building class data from {building_classes_file}!', 
              file=sys.stderr)
        # If reading the data failed, use placeholder data, so some 
        # functionality is maintained
        df = DEFAULT_BUILDING_CLASSES

    return df


# The observations dataframe should have at least the following columns:
#   class_id: same as building_classes class_id (string, unique)
#   [attribute]: number of observations of this attribute for a given class_id (integer)
DEFAULT_OBSERVATIONS = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                     '1': [1, 1, 1],
                                     '101': [1, 0, 1],
                                     '102': [0, 1, 0]})


def load_observations(observation_file, class_ids=(), attribute_ids=()):
    '''Attempts to load buiding-attribute observation data from file into Pandas dataframe'''
    try:
        df = pd.read_csv(observation_file, dtype={'class_id': str})

        # Check that the required fields are present
        assert 'class_id' in df
        for class_id in class_ids:
            assert class_id in df.class_id.values
        for attribute_id in attribute_ids:
            assert attribute_id in df.columns
    except:
        print(f'Failed to load observation data from {observation_file}!', 
                file=sys.stderr)
        # If reading the data failed, use placeholder data, so some 
        # functionality is maintained
        df = DEFAULT_OBSERVATIONS

    # Ensure that the column labels are interpreted as strings
    df.columns = df.columns.astype(str)

    return df


class BuildingData:
    def __init__(self, data_directory):
        '''Initializes a BuildingData object using the data files in data_directory'''
        # Load attribute data into hidden variable, access via properties
        attribute_file = os.path.join(data_directory, 'attributes.csv')
        self._attributes = load_attributes(attribute_file)

        # Load building class data into hidden variable, access via properties
        building_classes_file = os.path.join(data_directory, 'building_classes.csv')
        self._building_classes = load_building_classes(building_classes_file)

        # Load observation data
        observation_file = os.path.join(data_directory, 'observations.csv')
        self.observations = load_observations(observation_file, 
                                              class_ids=self._building_classes.class_id.unique(),
                                              attribute_ids=self._attributes.attribute_id.unique())

        # FIXME: if any of the previous give the default values, should force 
        # all of them to have default values, or simply fail?

    @property
    def attribute_name(self):
        '''Returns the attribute_id-attribute_name mapping'''
        return {attr_id:attr_name for ind,(attr_id, attr_name) in self._attributes.iterrows()}

    @property
    def building_class_name(self):
        '''Returns the building class_id-class_name mapping'''
        return {class_id:class_name for ind,(class_id, class_name) in self._building_classes.iterrows()}
