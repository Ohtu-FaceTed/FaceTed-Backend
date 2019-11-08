from src.sessionManagement import generate_id, users
from src.question_selection import next_question
from flask import jsonify, session
from . import views as app
from ..models import db, Session


@app.route('/question', methods=['GET'])
def question():
    # remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = generate_id()
    session['user'] = ident
    users[ident] = {'type': [], 'probabilities': [], 'answers': [],
                    'attributes': [], 'multi_attributes': [], 'question_strings': []}
    # Add the session to the database
    db.session.add(Session(ident))
    db.session.commit()
    question = next_question(None, [])
    if question['type'] == 'multi':
        users[ident]['type'].append('multi')
        users[ident]['multi_attributes'].append(question['attributes'])
    else:
        users[ident]['type'].append('simple')
        users[ident]['attributes'].append(question['attribute_id'])
    users[ident]['question_strings'].append(question['attribute_question'])
    
    return jsonify(question)
