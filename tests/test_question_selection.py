from src.question_selection import *
import pytest
from unittest import mock


@pytest.fixture
def attributes():
    attributes = pd.DataFrame({'attribute_id': ['1', '101', '102'],
                               'attribute_name': ['Asunnot', 'Asuinhuone',
                                                  'Eteinen'],
                               'attribute_question': ['Onko rakennuksessa asunnot?',
                                                      'Onko rakennuksessa asuinhuone?',
                                                      'Onko rakennuksessa eteinen?', ],
                               'group_id': ['NaN', 'NaN', 'NaN'],
                               'active': [False, False, False]})
    return attributes


def test_best_questions_is_ordered():
    questions = best_questions(None, [])
    for i in range(1, len(questions)):
        assert questions[i][1] >= questions[i - 1][1]


def test_for_simple_question_next_question_is_first_of_best_questions():
    questions = best_questions(None, [])
    best_question = next_question(None, [])
    if best_question['type'] == 'simple':
        assert best_question['attribute_id'] == questions[0][0]


def test_non_active_attributes_are_not_selected(attributes):
    #r = mock.Mock()
    #r.content = attributes
    # print(src.building_data.__dict__)
    # with mock.patch.('src.question_selection.src.building_data', '_attributes', new=attributes) as attr:
    tmp = src.building_data._attributes.copy()
    src.building_data._attributes = attributes

    questions = best_questions(None, [])
    attribute_id = []
    for q in questions:
        attribute_id.append(q[0])
    assert '1' not in attribute_id

    src.building_data._attributes = tmp


# def test_for_multi_question_first_of_best_questions_is_in_question_group():
#    questions = best_questions(None, [])
#    best_question = next_question(None, [])
#    if best_question['type'] == 'multi':
#        attributes = []
#        for attribute in best_question['attributes']:
#            attributes.append(attribute['attribute_id'])
#        assert questions[0][0] in attributes
