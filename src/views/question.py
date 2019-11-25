import json
from src.sessionManagement import generate_id, users
from src.question_selection import next_question
from flask import jsonify, session, request
from . import views as app
from . import select_question_by_language, get_best_match_language
from ..models import db, Session


@app.route('/question', methods=['GET'])
def question():
    best_match_language = get_best_match_language(request)

    # remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = generate_id()
    session['user'] = ident
    users[ident] = {'server_responses': [], 'user_responses': []}
    # Add the session to the database
    db.session.add(Session(ident))
    db.session.commit()
    question = next_question(None, [])

    questions = json.loads(question['attribute_question'])
    lang_parsed_question = select_question_by_language(
        question['attribute_question'], best_match_language)
    question['attribute_question'] = lang_parsed_question
    users[ident]['server_responses'].append(question)

    return jsonify(question)
