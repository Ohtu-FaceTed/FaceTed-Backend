import pytest
import numpy as np

@pytest.fixture
def attributes():
  from data.data import attributes
  return attributes

@pytest.fixture
def building_classes_numpy():
  from data.data import building_classes_numpy
  return building_classes_numpy

def test_attributes_are_returned_as_dictionary(attributes):
  assert type(attributes()) == dict

def test_building_classes_are_returned_as_numpy_array(building_classes_numpy):
  assert type(building_classes_numpy()) == np.ndarray
