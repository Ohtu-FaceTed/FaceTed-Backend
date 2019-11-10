from flask import session
from src.models import Session


def test_post_feedback_requires_json(backend):
    backend.get('/question')
    res = backend.post('/feedback')
    assert(res.get_json()['success'] == False)

def test_post_feedback_requires_class_id(backend):
    backend.get('/question')
    res = backend.post('/feedback', json={})
    assert(res.get_json()['success'] == False)

def test_post_feedback_requires_session(backend):
    with backend.session_transaction() as sess:
        sess.pop('user', None)
        assert 'user' not in sess
    res = backend.post('/feedback', json={
        'class_id': '0110'
    })
    assert(res.get_json()['success'] == False)

def test_post_feedback_succeeds(backend):
    backend.get('/question')
    res = backend.post('/feedback', json={
        'class_id': '0110'
    })
    assert(res.get_json()['success'] == True)

def test_post_feedback_ends_session(backend):
    with backend:
        backend.get('/question')
        assert 'user' in session
        backend.post('/feedback', json={
            'class_id': '0110'
        })
        assert 'user' not in session

def test_post_feedback_saves_selected_class(backend):
    users_session = None
    with backend:
        backend.get('/question')
        with backend.session_transaction() as sess:
            users_session = Session.query.filter_by(session_ident=sess['user']).first()
        assert users_session.selected_class == None
        backend.post('/feedback', json={
            'class_id': '0110'
        })
        assert users_session.selected_class.class_id == '0110'
