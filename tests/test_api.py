import src
from src import create_app
from flask import session
from src.sessionManagement import users
from config import TestingConfig
import pytest


@pytest.fixture(scope='module')
def backend():
    app = create_app(TestingConfig)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    ctxt.pop()

@pytest.fixture
def first_question(backend):
    responses = {'id': '', 'type': [], 'probabilities': [], 'multi_attributes': [],
                 'answers': [], 'questions': [], 'question_strings': [], 'attributes': [], 'total_attributes': []}
    attribute_id = []

    with backend:
        response = backend.get('/question')
        json = response.get_json()
        responses['id'] = session['user']
        question_type = json['type']
    
        if question_type == 'simple':
            attribute_id.append(json['attribute_id'])
            responses['questions'].append(json['attribute_name'])
            responses['total_attributes'].append(json['attribute_id'])
            responses['type'].append(question_type)
        else:
            responses['multi_attributes'].append(json['attributes'])
            for attribute in json['attributes']:
                attribute_id.append(attribute['attribute_id'])
                responses['total_attributes'].append(attribute['attribute_id'])
        responses['question_strings'].append(
            json['attribute_question'])

    return responses, attribute_id

@pytest.fixture
def next_questions(backend, first_question):
    responses = first_question[0]
    attribute_id = first_question[1]
    question_type = responses['type']

    for x in range(3):
        answer = []
        response = None

        with backend:
            if question_type == 'simple':
                answer = ['yes']
                response = backend.post(
                    '/answer', json={'language': 'suomi', 'response': [{'attribute_id': attribute_id, 'response': answer}]}
                    )
            else:
                multi_answer = []
                for attribute in attribute_id:
                    res = {'attribute_id': attribute, 'response': 'no'}
                    multi_answer.append(res)
                    answer.append('no')
                    response = backend.post(
                        '/answer', json={'language': 'suomi', 'response': multi_answer}
                        )

            json = response.get_json()

            if json['new_question']['type'] == 'simple':
                question_type = 'simple'
                attribute_id = json['new_question']['attribute_id']
                responses['attributes'].append(attribute_id)
                responses['total_attributes'].append(attribute_id)
                responses['questions'].append(
                    json['new_question']['attribute_name'])
            else:
                question_type = 'multi'
                multi_id = []
                for attribute in json['new_question']['attributes']:
                    multi_id.append(attribute['attribute_id'])
                    attribute_id = multi_id
                    responses['multi_attributes'].append(json['new_question']['attributes'])
                    responses['total_attributes'].append(attribute['attribute_id'])

            responses['question_strings'].append(
                json['new_question']['attribute_question'])               
            if len(responses['probabilities']) > 0:
                prior = responses['probabilities'][-1]
            posterior = src.classifier.calculate_posterior(
                attribute_id, answer, prior)
            new = posterior['posterior']
            responses['probabilities'].append(new)
            responses['answers'].append(answer)
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
    if json['type'] == 'simple':
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
        '/answer', json={"language":"suomi","response":[{"attribute_id": "1", "response": "yes"}]}
    )
    json = response.get_json()
    assert json['success'] == True


def test_post_answer_returns_new_question(backend):
    response = backend.post(
        '/answer', json={"language":"suomi","response":[{"attribute_id": "1", "response": "yes"}]}
    )
    json = response.get_json()
    assert 'new_question' in json
    assert 'type' in json['new_question']
    assert 'attribute_question' in json['new_question']
    if json['new_question']['type'] == 'simple':
        assert 'attribute_id' in json['new_question']
        assert 'attribute_name' in json['new_question']

def test_post_answer_returns_building_classes(backend):
    response = backend.post(
        '/answer', json={"language": "suomi", "response": [{"attribute_id": "1", "response": "yes"}]}
    )
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


def test_if_user_in_session_user_data_is_created_after_first_question(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            users.pop(session['user'], None)
            assert session['user'] not in users
            backend.post(
                '/answer', json={"language": "suomi", "response": [{"attribute_id": attribute_id, "response": "yes"}]}
                )
            assert session['user'] in users


def test_same_questions_not_repeated_during_session(next_questions):
    questions = next_questions['question_strings']
    attributes = next_questions['total_attributes']
    unique_questions = list(set(questions))
    unique_attributes = list(set(attributes))
    assert len(unique_questions) == len(questions)
    assert len(unique_attributes) == len(attributes)


def test_prior_questions_are_saved_during_session(next_questions):
    user = users[next_questions['id']]
    assert user['total_attributes'] == next_questions['total_attributes']


def test_prior_question_strings_are_saved_during_session(next_questions):
    user = users[next_questions['id']]
    assert user['question_strings'] == next_questions['question_strings']


def test_users_answers_are_saved_during_session(next_questions):
    user = users[next_questions['id']]
    assert user['answers'] == next_questions['answers']


def test_prior_probabilities_are_saved_during_session(next_questions):
    user = users[next_questions['id']]
    prob = user['probabilities']
    comp = next_questions['probabilities']
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
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            prob = src.classifier.calculate_posterior(attribute_id, 'yes', None)
            prior = prob['posterior']
            response = backend.post(
                '/answer', json={"language":"suomi","response":[{"attribute_id":attribute_id,"response":"yes"}]})
            json = response.get_json()
            attribute_id = json['new_question']['attribute_id']
            posterior = src.classifier.calculate_posterior(
                attribute_id, 'yes', prior)
            response = backend.post(
                '/answer', json={"language":"suomi","response":[{"attribute_id":attribute_id,"response":"yes"}]})
            json = response.get_json()
            building_classes = json['building_classes']
            for _, (class_id, score) in posterior.iterrows():
                new_building_classes.append({'class_id': class_id,
                                            'class_name': src.building_data.building_class_name[class_id],
                                            'score': score})
            assert building_classes == new_building_classes


def test_requesting_previous_question_returns_correct_question(next_questions, backend):
    previous_question_string = next_questions['question_strings'][-2]
    previous_type = next_questions['type'][-2]
    previous_attribute = ''
    previous_question = ''
    if previous_type == 'simple':
        previous_attribute = next_questions['attributes'][-2]
        previous_question = next_questions['questions'][-2]
    else:
        previous_attribute = next_questions['multi_attributes'][-2]
    with backend:
        response = backend.get('/previous')
        json = response.get_json()
        if json['type'] == 'simple':
            question = json['new_question']['attribute_name']
            attribute = json['new_question']['attribute_id']
            question_string = json['new_question']['attribute_question']
            assert question == previous_question
            assert attribute == previous_attribute
            assert question_string == previous_question_string
        else:
            attribute = json['new_question']['attributes']
            assert attribute == previous_attribute


def test_if_user_returs_to_first_question_no_building_classes_are_sent(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            question = json['attribute_name']
            attribute_id = json['attribute_id']
            backend.post(
                '/answer', json={"language":"suomi","response":[{"attribute_id":attribute_id,"response":"yes"}]})
            previous = backend.get('/previous')
            json = previous.get_json()
            assert 'building_classes' not in json
            assert json['attribute_name'] == question


def test_if_user_in_session_user_data_is_created_when_asking_previous_question(backend):
    with backend:
        response = backend.get('/question')
        json = response.get_json()
        if json['type'] == 'simple':
            attribute_id = json['attribute_id']
            backend.post(
                '/answer', json={"language":"suomi","response":[{"attribute_id":attribute_id,"response":"yes"}]})
            users.pop(session['user'], None)
            assert session['user'] not in users
            backend.get('/previous')
            assert session['user'] in users

