import src
import json

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import jsonify, session, request
from . import views as app
#from ..models import db, Attribute, Session, QuestionGroup, AnswerQuestion
#from . import get_best_match_language, select_question_by_language


#def fix_question_language(question, language):
#    if question['type'] == 'multi':
#        question['attribute_question'] = select_question_by_language(
#            question['attribute_question'], language)
#        for attribute in question['attributes']:
#            attribute['attribute_name'] = select_question_by_language(
#                attribute['attribute_name'], language)
#    else:
#        question['attribute_question'] = select_question_by_language(
#            question['attribute_question'], language)


@app.route('/previous', methods=['GET'])
def previous():
    user = None
    #prior = None
    #attribute_id = []
    #response = []

    #browser_languages = request.accept_languages
    #best_match_language = get_best_match_language(browser_languages)

    if 'user' in session:
        # access users session data
        if session['user'] in users:
            user = users[session['user']]
        else:
            ident = generate_id()
            session['user'] = ident
            users[ident] = {'server_responses': [], 'user_responses': []}

            user = users[ident]

    # if user has no previous data a new question is created and saved
    if len(user['server_responses']) == 0:
        question = next_question(None, [])
        users[ident]['server_responses'].append(question)
        return jsonify(question)

    if len(user['server_responses']) == 1:
        question = user['server_responses'][-1]
        return jsonify(question)

    # if user returns to the first question, only the question is returned
    if len(user['server_responses']) == 2 and len(user['user_responses']) == 1:
        user['server_responses'].pop()
        user['user_responses'].pop()

        question = user['server_responses'][-1]
        return jsonify(question)
  
    if len(user['server_responses']) > 2 and len(user['user_responses']) > 1:
        user['server_responses'].pop()
        user['user_responses'].pop()

        question = user['server_responses'][-1]
        question['success'] = True
        return jsonify(question)
