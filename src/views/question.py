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
    users[ident] = {'probabilities': [], 'answers': [],
                    'questions': [], 'question_strings': [], 'attributes': [],
                    'db_session': Session(ident)}
    # Add the session to the database
    db.session.add(users[ident]['db_session'])
    db.session.commit()
    question = next_question(None, [])
    users[ident]['questions'].append(question['attribute_name'])
    users[ident]['question_strings'].append(question['attribute_question'])
    users[ident]['attributes'].append(question['attribute_id'])
    return jsonify(question)
