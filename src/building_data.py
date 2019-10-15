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


def load_attributes(attribute_file, verbose=True):
    '''Attempts to load attribute data from file into Pandas dataframe'''
    df = None
    try:
        df = pd.read_csv(attribute_file, dtype=str)

        # Check that the required fields are present
        if 'attribute_id' not in df:
            raise ValueError(
                "The attributes data does not contain a 'attribute_id' column!")
        if 'attribute_name' not in df:
            raise ValueError(
                "The attributes data does not contain a 'attribute_name' column!")
        if 'attribute_question' not in df:
            raise ValueError(
                "The attributes data does not contain a 'attribute_question' column")
    except ValueError as e:
        if verbose:
            print(f'The attribute file ({attribute_file}) failed to meet expectations: {e.args[0]}',
                  file=sys.stderr)
        df = None  # Reset to None so that we substitute the default dataframe
    except Exception:
        if verbose:
            print(f'Failed to load attribute data from {attribute_file}!',
                  file=sys.stderr)
    finally:
        # If reading the data failed, use placeholder data, so some
        # functionality is maintained
        if df is None:
            if verbose:
                print('Substituting placeholder data for attributes!',
                      file=sys.stderr)
            df = DEFAULT_ATTRIBUTES

    return df


# The building classes dataframe should have at least the following fields:
#   class_id: four digit class identifier (string, unique)
#   class_name: common name for class (string)
DEFAULT_BUILDING_CLASSES = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                         'class_name': ['Omakotitalot',
                                                        'Paritalot',
                                                        'Rivitalot']})


def load_building_classes(building_classes_file, verbose=True):
    '''Attempts to load buiding class data from file into Pandas dataframe'''
    df = None
    try:
        df = pd.read_csv(building_classes_file, dtype=str)
        # Check that the required fields are present
        if 'class_id' not in df:
            raise ValueError(
                "The building classes data does not contain a 'class_id' column!")
        if 'class_name' not in df:
            raise ValueError(
                "The building classes data does not contain a 'class_name' column!")
    except ValueError as e:
        if verbose:
            print(f'The building classes file ({building_classes_file}) failed to meet expectations: {e.args[0]}',
                  file=sys.stderr)
        df = None  # Reset to None so that we substitute the default dataframe
    except Exception:
        if verbose:
            print(f'Failed to load building class data from {building_classes_file}!',
                  file=sys.stderr)
    finally:
        # If reading the data failed, use placeholder data, so some
        # functionality is maintained
        if df is None:
            if verbose:
                print('Substituting placeholder data for building classes!',
                      file=sys.stderr)
            df = DEFAULT_BUILDING_CLASSES

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


def load_observations(observation_file, class_ids=None, attribute_ids=None, verbose=True):
    '''Attempts to load buiding-attribute observation data from file into Pandas dataframe'''
    df = None
    try:
        df = pd.read_csv(observation_file, dtype={'class_id': str})

        # Check that the class_id and count fields are present
        if 'class_id' not in df:
            raise ValueError(
                "The observation data does not contain a 'class_id' column!")
        if 'count' not in df:
            raise ValueError(
                "The observation data does not contain a 'count' column!")

        # Check counts are positive integers
        if not np.equal(np.mod(df['count'], 1), 0).all or (df['count'] < 1).any():
            raise ValueError(
                "Found 'count' values in observation data that are not positive integers")

        # If class_ids is given, check that we find all the ids in the
        # observations in class_ids as well
        if class_ids is not None:
            for class_id in df.class_id.unique():
                if class_id not in class_ids:
                    raise ValueError(
                        f'The class id {class_id} is only found in observations!')
        # If attribute_ids is given, check that we find all the ids in the
        # observations in attribute_ids as well
        if attribute_ids is not None:
            for attribute_id in df.columns:
                if attribute_id in ['class_id', 'count']:
                    continue
                if attribute_id not in attribute_ids:
                    raise ValueError(
                        f'The attribute id {attribute_id} is only found in observations!')
    except ValueError as e:
        if verbose:
            print(f'The observation data file ({observation_file}) failed to meet expectations: {e.args[0]}',
                  file=sys.stderr)
        df = None  # Reset to None so that we substitute the default dataframe
    except Exception:
        if verbose:
            print(f'Failed to load observation data from {observation_file}!',
                  file=sys.stderr)
    finally:
        # If reading the data failed, use placeholder data, so some
        # functionality is maintained
        if df is None:
            if verbose:
                print('Substituting placeholder data for observations!',
                      file=sys.stderr)
            df = DEFAULT_OBSERVATIONS

    # Ensure that the column labels are interpreted as strings
    df.columns = df.columns.astype(str)

    return df


class BuildingData:
    def __init__(self, data_directory, verbose=True):
        '''Initializes a BuildingData object using the data files in data_directory'''
        # Load attribute data into hidden variable, access via properties
        attribute_file = os.path.join(data_directory, 'attributes.csv')
        self._attributes = load_attributes(attribute_file, verbose=verbose)
        self._attributes_dict = {attr_id: {'attribute_id': attr_id,
                                           'attribute_name': attr_name,
                                           'attribute_question': attr_question}
                                 for ind, (attr_id, attr_name, attr_question) in self._attributes.iterrows()}
        self._attributes_names_dict = {attr_id: attr_name for ind,
                                       (attr_id, attr_name, attr_question) in self._attributes.iterrows()}

        # Load building class data into hidden variable, access via properties
        building_classes_file = os.path.join(
            data_directory, 'building_classes.csv')
        self._building_classes = load_building_classes(
            building_classes_file, verbose=verbose)
        self._building_classes_dict = {class_id: class_name for ind,
                                       (class_id, class_name) in self._building_classes.iterrows()}

        # Load observation data
        observation_file = os.path.join(data_directory, 'observations.csv')
        self.observations = load_observations(observation_file,
                                              class_ids=self._building_classes.class_id.unique(),
                                              attribute_ids=self._attributes.attribute_id.unique(),
                                              verbose=verbose)

        # FIXME: if any of the previous give the default values, should force
        # all of them to have default values, or simply fail?

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
