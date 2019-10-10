from src import app
from flask import session
from src.sessionManagement import users
from src.question_selection import *
import src
import pytest

@pytest.fixture(scope='module')
def backend():
    app.config['TESTING'] = True

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()

def test_best_question_has_lower_entropy_than_remaining_questions(backend):
    with backend:
        response = backend.get('/question')
        ident = response.get_json()['attribute_id']
        questions = best_questions()
        while questions:
            entropy = new_entropy(ident)
            assert entropy <= max(questions, key=lambda x: x[1])[1]
            response = backend.post('/answer', json={'language': 'suomi', 'attribute_id': ident, 'response': 'yes'})
            ident = response.get_json()['new_question']['attribute_id']
            questions = best_questions()
