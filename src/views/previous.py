import src
#from src import app

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import jsonify, session
from . import views as app
from ..models import db, Attribute, Session, QuestionGroup


@app.route('/previous', methods=['GET'])
def previous():
    user = None
    prior = None
    attribute_id = ''
    response = ''
    question_type = 'simple'

    if 'user' in session:
        # access users session data
        if session['user'] in users:
            user = users[session['user']]
        else:
            ident = generate_id()
            session['user'] = ident
            users[ident] = {'type': [], 'probabilities': [], 'answers': [], 
                                'attributes': [], 'multi_attributes': [], 'question_strings': []}
            user = users[ident]

    # if user has no previous data a new question is created and saved
    if len(user['question_strings']) == 0:
        question = next_question(None, [])
        if question['type'] == 'multi':
            user['type'].append('multi')
            user['multi_attributes'].append(question['attributes'])
        else:
            user['type'].append('simple')
            user['attributes'].append(question['attribute_id'])
        user['question_strings'].append(question['attribute_question']) 
        return jsonify(question)

    # if user returns to the first question, only the question is returned
    if len(user['probabilities']) < 2 and len(user['questions_strings']) > 0:
        if len(user['probabilities']) == 1:
            user['probabilities'].pop()
        user['multi_attributes'].pop() if user['type'][-1] == 'multi' else user['attributes'].pop() and user['questions'].pop()
        user['question_strings'].pop()

        if user['type'][-1] == 'multi':
            return {"type": 'multi', "attributes": user['multi_attributes'][-1], 
                    "attribute_question":  user['question_strings'][-1]}

        else:
            db_attribute = Attribute.query.filter_by(attribute_id=user['attributes'][-1]).first()
            return {"type": 'simple', "attribute_id": user['attributes'][-1], "attribute_name":  db_attribute.attribute_name,
                    "attribute_question": user['question_strings'][-1]}

    # deletes previously saved values
    user['probabilities'] = user['probabilities'][: -2]
    if user['type'][-1] == 'multi':
        user['multi_attributes'].pop()
    else:
        user['answers'].pop()
        user['attributes'] = user['attributes'][: -2]
    #user['questions'] = user['questions'][: -2]
    user['question_strings'] = user['question_strings'][: -2]
    

    # selects the values that led to previous probabilities
    if len(user['probabilities']) > 0:
        prior = user['probabilities'][-1]
    if user['type'][-1] == 'multi':
        attribute_id = user['multi_attributes'][-1]
        response = user['answers'][-1]
    else:
        attribute_id = [user['attributes'][-1]]
        response = [user['answers'][-1]]

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
    db_session = Session.query.filter_by(session_ident=session['user']).first()
    answered = [question.attribute_id for question in db_session.answered_questions]
    question = next_question(user['probabilities'][-1], answered)
    user['question_strings'].append(question['attribute_question'])

    if question['type'] == 'multi':
        user['multi_attributes'].append(question['attributes'])
    else:
        user['attributes'].append(question['attribute_id'])

    return jsonify({'success': True,
                    'new_question': question,
                    'building_classes': new_building_classes})
