from src.question_selection import *
import pytest


def test_best_questions_is_ordered():
    questions = best_questions(None, [])
    for i in range(1, len(questions)):
        assert questions[i][1] >= questions[i - 1][1]


def test_for_simple_question_next_question_is_first_of_best_questions():
    questions = best_questions(None, [])
    best_question = next_question(None, [])
    if best_question['type'] == 'simple':
        assert best_question['attribute_id'] == questions[0][0]


#def test_for_multi_question_first_of_best_questions_is_in_question_group():
#    questions = best_questions(None, [])
#    best_question = next_question(None, [])
#    if best_question['type'] == 'multi':
#        attributes = []
#        for attribute in best_question['attributes']:
#            attributes.append(attribute['attribute_id'])
#        assert questions[0][0] in attributes


