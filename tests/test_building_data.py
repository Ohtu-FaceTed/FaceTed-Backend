from src.building_data import *
import pytest
import pandas as pd


@pytest.fixture
def default_attributes():
    return load_attributes(None)

def test_attributes_is_dataframe(default_attributes):
    assert isinstance(default_attributes, pd.DataFrame)

def test_attribute_dataframe_is_not_empty(default_attributes):
    assert default_attributes.shape[1] > 0

def test_attribute_dataframe_has_attribute_id(default_attributes):
    assert 'attribute_id' in default_attributes

def test_attribute_dataframe_has_attribute_name(default_attributes):
    assert 'attribute_name' in default_attributes

def test_attribute_dataframe_values_are_strings(default_attributes):
    for x in default_attributes.attribute_id:
        assert isinstance(x, str)
    for x in default_attributes.attribute_name:
        assert isinstance(x, str)


@pytest.fixture
def default_building_classes():
    return load_building_classes(None)

def test_building_classes_is_dataframe(default_building_classes):
    assert isinstance(default_building_classes, pd.DataFrame)

def test_building_classes_dataframe_is_not_empty(default_building_classes):
    assert default_building_classes.shape[1] > 0

def test_building_classes_dataframe_has_class_id(default_building_classes):
    assert 'class_id' in default_building_classes

def test_building_classes_dataframe_has_class_name(default_building_classes):
    assert 'class_name' in default_building_classes

def test_building_classes_dataframe_values_are_strings(default_building_classes):
    for x in default_building_classes.class_id:
        assert isinstance(x, str)
    for x in default_building_classes.class_name:
        assert isinstance(x, str)


@pytest.fixture
def default_observations():
    return load_observations(None)

def test_observations_is_dataframe(default_observations):
    assert isinstance(default_observations, pd.DataFrame)

def test_observations_has_at_least_one_building_class_and_attribute(default_observations):
    assert default_observations.shape[0] >= 1
    assert default_observations.shape[1] >= 1

def test_observations_class_ids_are_strings(default_observations):
    for x in default_observations.class_id:
        assert isinstance(x, str)


@pytest.fixture
def default_building_data():
    return BuildingData('')

def test_attribute_name_is_dict(default_building_data):
    assert isinstance(default_building_data.attribute_name, dict)

def test_building_class_name_is_dict(default_building_data):
    assert isinstance(default_building_data.building_class_name, dict)