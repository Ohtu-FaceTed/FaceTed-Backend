from app import app
from flask import jsonify, session
import pytest

@pytest.fixture(scope='module')
def backend():
    app.config['TESTING'] = True

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()

def test_get_root_succeeds(backend):
    response = backend.get('/')
    assert response.status_code == 200

def test_get_question_succeeds(backend):
    response = backend.get('/question')
    assert response.status_code == 200

def test_get_question_returns_json(backend):
    response = backend.get('/question')
    json = response.get_json()
    assert 'attribute_id' in json
    assert 'attribute_name' in json

def test_get_answer_fails(backend):
    response = backend.get('/answer')
    assert response.status_code == 405

def test_post_answer_succeeds(backend):
    response = backend.post('/answer')
    assert response.status_code == 200

def test_post_answer_requires_sent_json(backend):
    response = backend.post('/answer')
    json = response.get_json()
    assert json['success'] == False

def test_post_answer_requires_all_fields(backend):
    response = backend.post('/answer', json={'language': 1})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post('/answer', json={'language': 1, 'attribute_id': '1'})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post('/answer', json={'language': 1, 'attribute_id': '1', 'response': True})
    json = response.get_json()
    assert json['success'] == True

def test_post_answer_returns_new_question(backend):
    response = backend.post('/answer', json={'language': 1, 'attribute_id': '1', 'response': True})
    json = response.get_json()
    assert 'new_question' in json
    assert 'attribute_id' in json['new_question']
    assert 'attribute_name' in json['new_question']

def test_post_answer_returns_building_classes(backend):
    response = backend.post('/answer', json={'language': 1, 'attribute_id': '1', 'response': True})
    json = response.get_json()
    assert 'building_classes' in json
    for item in json['building_classes']:
        assert 'class_id' in item
        assert 'class_name' in item
        assert 'score' in item

def test_session_gets_created_for_client_requesting_first_question(backend):
    with backend:
        backend.get('/question')
        assert 'user' in session

def test_id_stored_in_session_is_string(backend):
    with backend:
        backend.get('/question')
        assert type(session['user']) == str

def test_session_gets_recreated_for_client_requesting_first_question(backend):
    previous_id = ''
    with backend:
        backend.get('/question')
        with backend.session_transaction() as sess:
            previous_id = sess['user']
        backend.get('/question')
        assert previous_id != ''
        assert session['user'] != previous_id
