import src
from src import app
from flask import session
from src.sessionManagement import users
import pytest


@pytest.fixture(scope='module')
def backend():
    app.config['TESTING'] = True

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()


@pytest.fixture
def responses(backend):
    responses = {'id': '', 'probabilities': [],
                 'answers': [], 'questions': [], 'attributes': []}
    answer = 'yes'
    prior = None
    attribute_id = ''
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        responses['id'] = session['user']
        attribute_id = json['attribute_id']
        responses['questions'].append(json['attribute_name'])
        for x in range(3):
            response = backend.post(
                '/answer', json={'language': 'suomi', 'attribute_id': attribute_id, 'response': answer})
            json = response.get_json()
            attribute_id = json['new_question']['attribute_id']
            responses['questions'].append(
                json['new_question']['attribute_name'])
            responses['attributes'].append(attribute_id)
            if len(responses['probabilities']) > 0:
                prior = responses['probabilities'][-1]
            posterior = src.classifier.calculate_posterior(
                attribute_id, answer, prior)
            new = posterior['posterior']
            responses['probabilities'].append(new)
            responses['answers'].append(answer)
            if answer == 'yes':
                answer = 'now'
    return responses


def test_get_root_succeeds(backend):
    response = backend.get('/')
    assert response.status_code == 200


def test_get_question_succeeds(backend):
    print('here')
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
    response = backend.post('/answer', json={})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post('/answer', json={'attribute_id': '1'})
    json = response.get_json()
    assert json['success'] == False

    response = backend.post(
        '/answer', json={'attribute_id': '1', 'response': 'yes'})
    json = response.get_json()
    assert json['success'] == True


def test_post_answer_returns_new_question(backend):
    response = backend.post(
        '/answer', json={'language': 1, 'attribute_id': '1', 'response': 'yes'})
    json = response.get_json()
    assert 'new_question' in json
    assert 'attribute_id' in json['new_question']
    assert 'attribute_name' in json['new_question']


def test_post_answer_returns_building_classes(backend):
    response = backend.post(
        '/answer', json={'language': 1, 'attribute_id': '1', 'response': 'yes'})
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
        assert isinstance(session['user'], str)


def test_session_gets_recreated_for_client_requesting_first_question(backend):
    previous_id = ''
    with backend:
        backend.get('/question')
        with backend.session_transaction() as sess:
            previous_id = sess['user']
        backend.get('/question')
        assert previous_id != ''
        assert session['user'] != previous_id

<<<<<<< HEAD
def test_if_user_in_session_user_data_is_created_after_first_question(backend):
    with backend:
        backend.get('/question')
        users.pop(session['user'], None)
        assert session['user'] not in users
        backend.post('/answer', json={'attribute_id': '1', 'response': 'yes'})
        assert session['user'] in users
=======
>>>>>>> lint

def test_same_questions_not_repeated_during_session(responses):
    questions = responses['questions']
    attributes = responses['attributes']
    unique_questions = list(set(questions))
    unique_attributes = list(set(attributes))
    assert len(unique_questions) == len(questions)
    assert len(unique_attributes) == len(attributes)


def test_prior_questions_are_saved_during_session(responses):
    user = users[responses['id']]
    assert user['questions'] == responses['questions']


def test_users_answers_are_saved_during_session(responses):
    user = users[responses['id']]
    assert user['answers'] == responses['answers']


def test_prior_probabilities_are_saved_during_session(responses):
    user = users[responses['id']]
    prob = user['probabilities']
    comp = responses['probabilities']
    assert len(prob) == len(comp)


def test_returned_building_classes_are_based_on_prior_probabilities(backend):
    attribute_id = ''
    response = ''
    prior = ''
    posterior = ''
    building_classes = []
    new_building_classes = []
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        attribute_id = json['attribute_id']
        prob = src.classifier.calculate_posterior(attribute_id, 'yes', None)
        prior = prob['posterior']
        response = backend.post(
            '/answer', json={'language': 'suomi', 'attribute_id': attribute_id, 'response': 'yes'})
        json = response.get_json()
        attribute_id = json['new_question']['attribute_id']
        posterior = src.classifier.calculate_posterior(
            attribute_id, 'yes', prior)
        response = backend.post(
            '/answer', json={'language': 'suomi', 'attribute_id': attribute_id, 'response': 'yes'})
        json = response.get_json()
        building_classes = json['building_classes']
        for _, (class_id, score) in posterior.iterrows():
            new_building_classes.append({'class_id': class_id,
                                         'class_name': src.building_data.building_class_name[class_id],
                                         'score': score})
        assert building_classes == new_building_classes
