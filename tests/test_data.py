import pytest
import numpy as np
import pandas as pd

@pytest.fixture
def attributes():
  from data.data import attributes
  return attributes

@pytest.fixture
def building_observations():
  from data.data import building_observations
  return building_observations

@pytest.fixture
def building_classes():
  from data.data import building_classes
  return building_classes

@pytest.fixture
def conditional_probabilities():
  from data.data import conditional_probabilities
  return conditional_probabilities

@pytest.fixture
def calculate_posterior():
  from data.data import calculate_posterior
  return calculate_posterior

def test_attributes_is_a_dictionary(attributes):
  assert type(attributes) == dict

def test_attributes_is_not_empty(attributes):
  assert len(attributes) > 0

def test_attributes_keys_and_values_are_strings(attributes):
  for key,value in attributes.items():
    assert type(key) == str
    assert type(value) == str

def test_building_observations_is_dataframe(building_observations):
  assert type(building_observations) == pd.DataFrame

def test_building_observations_has_at_least_one_building_class_and_attribute(building_observations):
  assert building_observations.ndim == 2
  assert building_observations.shape[0] >= 1
  assert building_observations.shape[1] >= 1

def test_building_classes_is_a_dictionary(building_classes):
  assert type(building_classes) == dict

def test_building_classes_is_not_empty(building_classes):
  assert len(building_classes) > 0

def test_building_classes_keys_and_values_are_strings(building_classes):
  for key,value in building_classes.items():
    assert type(key) == str
    assert type(value) == str

def test_conditional_probabilities_is_pandas_dataframe(conditional_probabilities):
  assert type(conditional_probabilities) == pd.DataFrame

def test_conditional_probabilities_has_at_least_one_building_class_and_attribute(conditional_probabilities):
  assert conditional_probabilities.ndim == 2
  assert conditional_probabilities.shape[0] >= 1
  assert conditional_probabilities.shape[1] >= 1

def test_conditional_probabilities_class_ids_in_building_classes(conditional_probabilities, building_classes):
  for class_id in conditional_probabilities['class_id']:
    assert class_id in building_classes.keys()

def test_conditional_probabilities_attribute_ids_in_attributes(conditional_probabilities, attributes):
  for attribute_id in conditional_probabilities.columns:
    assert attribute_id == 'class_id' or attribute_id in attributes.keys()

def test_calculate_posterior_normalizes_probabilities_by_default(calculate_posterior):
  res = calculate_posterior("1", True)
  assert np.isclose(res['posterior'].sum(), 1.0)

def test_calculate_posterior_unnormalized_probabilities_are_probabilities(calculate_posterior):
  res_true = calculate_posterior("1", True, normalize=False)
  assert (0 <= res_true['posterior']).all() and (res_true['posterior'] <= 1).all()
  res_false = calculate_posterior("1", False, normalize=False)
  assert (0 <= res_false['posterior']).all() and (res_false['posterior'] <= 1).all()

def test_calculate_posterior_unnormalized_probabilities_are_bernoulli(calculate_posterior):
  res_true = calculate_posterior("1", True, normalize=False)
  res_false = calculate_posterior("1", False, normalize=False)
  assert np.isclose(res_true['posterior']+res_false['posterior'], 1.0).all()
  