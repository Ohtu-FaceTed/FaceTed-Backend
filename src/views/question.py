import json
from src.sessionManagement import create_session, users
from src.question_selection import next_question
from flask import jsonify, session, request
from . import views as app
from . import select_question_by_language, get_best_match_language


@app.route('/question', methods=['GET'])
def question():
    best_match_language = get_best_match_language(request)

    # Remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = create_session()
    question = next_question(None, [])

    questions = json.loads(question['attribute_question'])
    lang_parsed_question = select_question_by_language(
        question['attribute_question'], best_match_language)
    question['attribute_question'] = lang_parsed_question
    users[ident]['server_responses'].append(question)

    return jsonify(question)
