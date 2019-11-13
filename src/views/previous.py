import src
import json

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import jsonify, session, request
from . import views as app
from ..models import db, Attribute, Session, QuestionGroup
from . import get_best_match_language, select_question_by_language

def fix_question_language(question, language):
    if question['type'] == 'multi':
        question['attribute_question'] = select_question_by_language(question['attribute_question'], language)
        for attribute in question['attributes']:
            attribute['attribute_name'] = select_question_by_language(attribute['attribute_name'], language)
    else:
        question['attribute_question'] = select_question_by_language(question['attribute_question'], language)

@app.route('/previous', methods=['GET'])
def previous():
    user = None
    prior = None
    attribute_id = []
    response = []
    
    browser_languages = request.accept_languages
    best_match_language = get_best_match_language(browser_languages)

    if 'user' in session:
        # access users session data
        if session['user'] in users:
            user = users[session['user']]
        else:
            ident = generate_id()
            session['user'] = ident
            users[ident] = {'type': [], 'probabilities': [], 'answers': [],
                            'attribute_ids': [], 'attributes': [], 'multi_attributes': [], 'question_strings': [],
                            'total_attributes': []}
            user = users[ident]

    # if user has no previous data a new question is created and saved
    if len(user['question_strings']) == 0:
        question = next_question(None, [])
        if question['type'] == 'multi':
            user['type'].append('multi')
            user['multi_attributes'].append(question['attributes'])
            for attribute in question['attributes']:
                users[ident]['total_attributes'].append(
                    attribute['attribute_id'])
        else:
            user['type'].append('simple')
            user['attribute_ids'].append(question['attribute_id'])
            user['total_attributes'].append(question['attribute_id'])
            user['attributes'].append(question['attribute_name'])
        user['question_strings'].append(question['attribute_question'])
        return jsonify(question)

    # if user returns to the first question, only the question is returned
    if len(user['probabilities']) < 2 and len(user['question_strings']) > 0:
        if len(user['probabilities']) == 1:
            user['probabilities'].pop()
        if user['type'][-1] == 'multi':
            user['total_attributes'] = user['total_attributes'][: -
                                                                len(user['type'[-1]]) or None]
            user['multi_attributes'].pop()
        else:
            user['attribute_ids'].pop()
            user['attributes'].pop()
            user['total_attributes'].pop()
        user['question_strings'].pop()
        user['answers'].pop()
        user['type'].pop()

        if user['type'][-1] == 'multi':
            return {"type": 'multi', "attributes": user['multi_attributes'][-1],
                    "attribute_question": user['question_strings'][-1]}

        else:
            return {"type": 'simple', "attribute_id": user['attribute_ids'][-1], "attribute_name": user['attributes'][-1],
                    "attribute_question": user['question_strings'][-1]}

    # deletes previously saved values
    for i in range(2):
        if user['type'][-1] == 'multi':
            user['total_attributes'] = user['total_attributes'][: -
                                                                len(user['multi_attributes'][-1]) or None]
            user['multi_attributes'].pop()

        else:
            user['attribute_ids'].pop()
            user['attributes'].pop()
            user['total_attributes'].pop()

        user['type'].pop()
        user['probabilities'].pop()
        user['question_strings'].pop()

    user['answers'].pop()

    # selects the values that led to previous probabilities
    if len(user['probabilities']) > 0:
        prior = user['probabilities'][-1]
    if user['type'][-1] == 'multi':
        for attribute in user['multi_attributes'][-1]:
            attribute_id.append(attribute['attribute_id'])
    else:
        attribute_id = [user['attribute_ids'][-1]]

    response = user['answers'][-1]

    posterior = src.classifier.calculate_posterior(
        attribute_id, response, prior)
    probabilities = posterior['posterior']
    new_building_classes = []
    for _, (class_id, score) in posterior.iterrows():
        new_building_classes.append({'class_id': class_id,
                                     'class_name': src.building_data.building_class_name[class_id],
                                     'score': score})

    # Saves current state
    user['probabilities'].append(probabilities)
    question = next_question(
        user['probabilities'][-1], user['total_attributes'])

    if question['type'] == 'multi':
        user['type'].append('multi')
        user['multi_attributes'].append(question['attributes'])
        for attribute in question['attributes']:
            user['total_attributes'].append(attribute['attribute_id'])
    else:
        user['type'].append('simple')
        user['attribute_ids'].append(question['attribute_id'])
        user['total_attributes'].append(question['attribute_id'])
        user['attributes'].append(question['attribute_name'])

    user['question_strings'].append(question['attribute_question'])

    fix_question_language(question, best_match_language)

    return jsonify({'success': True,
                    'new_question': question,
                    'building_classes': new_building_classes})
    
    

