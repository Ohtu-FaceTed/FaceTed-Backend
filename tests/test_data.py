import pytest
import numpy as np

@pytest.fixture
def attributes():
  from data.data import attributes
  return attributes

@pytest.fixture
def building_observations():
  from data.data import building_observations
  return building_observations

def test_attributes_are_returned_as_dictionary(attributes):
  assert type(attributes) == dict

def test_observations_are_returned_as_numpy_array(building_observations):
  assert type(building_observations) == np.ndarray

