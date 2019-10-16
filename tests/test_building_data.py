import pandas as pd
import pytest
import tempfile
from src.building_data import *


def test_load_attributes_fails_without_attribute_id():
    df = DEFAULT_ATTRIBUTES.drop(columns=['attribute_id'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_attributes(tmp_file.name)


def test_load_attributes_fails_without_attribute_name():
    df = DEFAULT_ATTRIBUTES.drop(columns=['attribute_name'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_attributes(tmp_file.name)


def test_load_attributes_fails_without_attribute_question():
    df = DEFAULT_ATTRIBUTES.drop(columns=['attribute_question'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_attributes(tmp_file.name)


def test_load_attributes_fails_without_data_rows():
    df = DEFAULT_ATTRIBUTES.drop(index=[0, 1, 2])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_attributes(tmp_file.name)


@pytest.fixture
def default_attributes():
    df = DEFAULT_ATTRIBUTES
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        attributes = load_attributes(tmp_file.name)

    return attributes


def test_attributes_is_dataframe(default_attributes):
    assert isinstance(default_attributes, pd.DataFrame)


def test_attribute_dataframe_is_not_empty(default_attributes):
    assert len(default_attributes.index) > 0


def test_attribute_dataframe_has_attribute_id(default_attributes):
    assert 'attribute_id' in default_attributes


def test_attribute_dataframe_has_attribute_name(default_attributes):
    assert 'attribute_name' in default_attributes


def test_attribute_dataframe_values_are_strings(default_attributes):
    for x in default_attributes.attribute_id:
        assert isinstance(x, str)
    for x in default_attributes.attribute_name:
        assert isinstance(x, str)


def test_load_building_classes_fails_without_class_id():
    df = DEFAULT_BUILDING_CLASSES.drop(columns=['class_id'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_building_classes(tmp_file.name)


def test_load_building_classes_fails_without_class_name():
    df = DEFAULT_BUILDING_CLASSES.drop(columns=['class_name'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_building_classes(tmp_file.name)


def test_load_building_classes_fails_without_data_rows():
    df = DEFAULT_BUILDING_CLASSES.drop(index=[0, 1, 2])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_building_classes(tmp_file.name)


@pytest.fixture
def default_building_classes():
    df = DEFAULT_BUILDING_CLASSES
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        building_classes = load_building_classes(tmp_file.name)

    return building_classes


def test_building_classes_is_dataframe(default_building_classes):
    assert isinstance(default_building_classes, pd.DataFrame)


def test_building_classes_dataframe_is_not_empty(default_building_classes):
    assert len(default_building_classes.index) > 0


def test_building_classes_dataframe_has_class_id(default_building_classes):
    assert 'class_id' in default_building_classes


def test_building_classes_dataframe_has_class_name(default_building_classes):
    assert 'class_name' in default_building_classes


def test_building_classes_dataframe_values_are_strings(default_building_classes):
    for x in default_building_classes.class_id:
        assert isinstance(x, str)
    for x in default_building_classes.class_name:
        assert isinstance(x, str)


def test_load_observations_fails_without_class_id():
    df = DEFAULT_OBSERVATIONS.drop(columns=['class_id'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_observations(tmp_file.name)


def test_load_observations_fails_without_count():
    df = DEFAULT_OBSERVATIONS.drop(columns=['count'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_observations(tmp_file.name)


def test_load_observations_fails_without_an_attribute_column():
    df = DEFAULT_OBSERVATIONS.drop(columns=['1', '101', '102'])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_observations(tmp_file.name)


def test_load_observations_fails_without_data_rows():
    df = DEFAULT_OBSERVATIONS.drop(index=[0, 1, 2])
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_observations(tmp_file.name)


def test_load_observations_fails_if_a_count_is_zero():
    df = DEFAULT_OBSERVATIONS.copy()
    df.loc[1, 'count'] = 0
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        with pytest.raises(ValueError):
            load_observations(tmp_file.name)


@pytest.fixture
def default_observations():
    df = DEFAULT_OBSERVATIONS
    with tempfile.NamedTemporaryFile() as tmp_file:
        df.to_csv(tmp_file.name, index=False)
        observations = load_observations(tmp_file.name)

    return observations


def test_observations_is_dataframe(default_observations):
    assert isinstance(default_observations, pd.DataFrame)


def test_observations_dataframe_has_class_id(default_observations):
    assert 'class_id' in default_observations


def test_observations_dataframe_has_count(default_observations):
    assert 'count' in default_observations


def test_observations_has_at_least_one_building_class_and_attribute(default_observations):
    assert default_observations.shape[0] >= 1
    # class_id + count + [attributes]
    assert default_observations.shape[1] >= 3


def test_observations_class_ids_are_strings(default_observations):
    for x in default_observations.class_id:
        assert isinstance(x, str)


@pytest.fixture
def default_building_data():
    return BuildingData('')


def test_attribute_is_dict(default_building_data):
    assert isinstance(default_building_data.attribute, dict)


def test_attribute_keys_are_strings(default_building_data):
    for key in default_building_data.attribute.keys():
        assert isinstance(key, str)


def test_attribute_values_are_dict_with_attribute_fields(default_building_data):
    for value in default_building_data.attribute.values():
        assert isinstance(value, dict)
        for required_field in ['attribute_id', 'attribute_name', 'attribute_question']:
            assert required_field in value


def test_attribute_name_is_dict(default_building_data):
    assert isinstance(default_building_data.attribute_name, dict)


def test_building_class_name_is_dict(default_building_data):
    assert isinstance(default_building_data.building_class_name, dict)
