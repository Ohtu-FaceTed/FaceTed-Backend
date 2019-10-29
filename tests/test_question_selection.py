from src.question_selection import *
import pytest


def test_best_questions_is_ordered():
    questions = best_questions(None, [])
    for i in range(1, len(questions)):
        assert questions[i][1] >= questions[i-1][1]

def test_next_question_is_first_of_best_questions():
    questions = best_questions(None, [])
    best_question = next_question(None, [])
    assert best_question['attribute_id'] == questions[0][0]
 