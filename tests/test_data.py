import pytest
import numpy as np

@pytest.fixture
def attributes():
  from data.data import attributes
  return attributes

@pytest.fixture
def building_classes():
  from data.data import building_classes
  return building_classes

def test_attributes_are_returned_as_dictionary(attributes):
  assert type(attributes()) == dict

def test_building_classes_are_returned_as_numpy_array(building_classes):
  assert type(building_classes()) == np.ndarray
