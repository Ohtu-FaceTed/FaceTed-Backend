from src.building_data import *
import pytest


@pytest.fixture
def external_building_data():
    return BuildingData('./data/')

def test_observation_class_ids_in_building_classes(external_building_data):
  observations = external_building_data.observations
  building_class_name = external_building_data.building_class_name
  for class_id in observations['class_id']:
    assert class_id in building_class_name.keys()

def test_conditional_probabilities_attribute_ids_in_attributes(external_building_data):
  observations = external_building_data.observations
  attribute_name = external_building_data.attribute_name
  for attribute_id in observations.columns:
    assert attribute_id == 'class_id' or attribute_id in attribute_name.keys()



  