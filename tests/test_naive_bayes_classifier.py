import numpy as np
import pandas as pd
import pytest
from src.naive_bayes_classifier import *
from src.building_data import load_observations

@pytest.fixture
def default_conditional_probabilities():
    obs = load_observations(None)
    return calculate_conditional_probabilities(obs)

def test_conditional_probabilities_is_pandas_dataframe(default_conditional_probabilities):
    assert isinstance(default_conditional_probabilities, pd.DataFrame)

def test_conditional_probabilities_has_at_least_one_building_class_and_attribute(default_conditional_probabilities):
    assert default_conditional_probabilities.shape[0] >= 1
    assert default_conditional_probabilities.shape[1] >= 2 # class_id + (attributes)

def test_conditional_probabilities_are_probabilities(default_conditional_probabilities):
    for attribute in default_conditional_probabilities:
        if attribute in ['class_id', 'count']: continue
        p = default_conditional_probabilities[attribute]
        assert (0 <= p).all() and (p <= 1).all()


@pytest.fixture
def default_classifier():
    obs = load_observations(None)
    return NaiveBayesClassifier(obs)

def test_calculate_posterior_normalizes_probabilities_by_default(default_classifier):
    res = default_classifier.calculate_posterior("1", True)
    assert np.isclose(res['posterior'].sum(), 1.0)
    res = default_classifier.calculate_posterior("1", False)
    assert np.isclose(res['posterior'].sum(), 1.0)

def test_calculate_posterior_unnormalized_probabilities_are_probabilities(default_classifier):
    res_true = default_classifier.calculate_posterior("1", True, normalize=False)
    assert (0 <= res_true['posterior']).all() and (res_true['posterior'] <= 1).all()
    res_false = default_classifier.calculate_posterior("1", False, normalize=False)
    assert (0 <= res_false['posterior']).all() and (res_false['posterior'] <= 1).all()

def test_calculate_posterior_unnormalized_probabilities_are_bernoulli(default_classifier):
    res_true = default_classifier.calculate_posterior("1", True, normalize=False)
    res_false = default_classifier.calculate_posterior("1", False, normalize=False)
    assert np.isclose(res_true['posterior']+res_false['posterior'], 1.0).all()



