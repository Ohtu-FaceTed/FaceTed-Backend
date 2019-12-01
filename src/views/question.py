import json
from src.sessionManagement import generate_id, users
from src.question_selection import next_question
from flask import jsonify, session, request
from . import views as app
from . import get_best_match_language, fix_question_language
from ..models import db, Session


@app.route('/question', methods=['GET'])
def question():
    best_match_language = get_best_match_language(request)

    # remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = generate_id()
    session['user'] = ident
    users[ident] = {'type': [], 'probabilities': [], 'answers': [],
                    'attribute_ids': [], 'attributes': [], 'multi_attributes': [], 'question_strings': [],
                    'total_attributes': []}
    # Add the session to the database
    db.session.add(Session(ident))
    db.session.commit()
    question = next_question(None, [])
    fix_question_language(question, best_match_language)
    if question['type'] == 'multi':
        users[ident]['type'].append('multi')
        users[ident]['multi_attributes'].append(question['attributes'])
        for attribute in question['attributes']:
            users[ident]['total_attributes'].append(attribute['attribute_id'])
    else:
        users[ident]['type'].append('simple')
        users[ident]['attribute_ids'].append(question['attribute_id'])
        users[ident]['total_attributes'].append(question['attribute_id'])
        users[ident]['attributes'].append(question['attribute_name'])

    users[ident]['question_strings'].append(question['attribute_question'])

    return jsonify(question)
