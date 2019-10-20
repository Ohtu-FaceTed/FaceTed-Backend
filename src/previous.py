import src
from src import app

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import request, jsonify, session, redirect


@app.route('/previous', methods=['GET'])
def previous():
    user = None
    prior = None
    attribute_id = ''
    response = ''

    if 'user' in session:
        # access users session data
        if session['user'] in users:
            user = users[session['user']]
        else:
                ident = generate_id()
                session['user'] = ident
                users[ident] = {'probabilities': [],
                                'answers': [], 'questions': [], 'question_strings': [], 'attributes': []}
                user = users[ident]

    #if user has no previous data a new question is created and saved
    if len(user['questions']) == 0:
        question = next_question()
        users[ident]['questions'].append(question['attribute_name'])
        users[ident]['question_strings'].append(question['attribute_question'])
        users[ident]['attributes'].append(question['attribute_id'])
        return jsonify(question)

    #if user returns to the first question, only the question is returned
    if len(user['probabilities']) < 2 and len(user['questions']) > 0:
        if len(user['probabilities']) == 1:
            user['probabilities'].pop()
        user['attributes'].pop()
        user['questions'].pop()
        user['question_strings'].pop()
        attribute_id = user['attributes'][-1]
        question = user['questions'][-1]
        question_string = user['question_strings'][-1]
        return {"attribute_id": attribute_id, "attribute_name": question, "attribute_question": question_string}


    # deletes previously saved values
    user['probabilities'] = user['probabilities'][: -2]
    user['answers'].pop()
    user['questions'] = user['questions'][: -2]
    user['question_strings'] = user['question_strings'][: -2]
    user['attributes'] = user['attributes'][: -2]

    #selects the values that led to previous probabilities
    if len(user['probabilities']) > 0:
        prior = user['probabilities'][-1]
    attribute_id = user['attributes'][-1]
    response = user['answers'][-1]

    posterior = src.classifier.calculate_posterior(attribute_id, response, prior)
    probabilities = posterior['posterior']
    new_building_classes = []
    for _, (class_id, score) in posterior.iterrows():
        new_building_classes.append({'class_id': class_id,
                                     'class_name': src.building_data.building_class_name[class_id],
                                     'score': score})

    # Saves current state
    user['probabilities'].append(probabilities)
    question = next_question()
    user['questions'].append(question['attribute_name'])
    user['question_strings'].append(question['attribute_question'])
    user['attributes'].append(question['attribute_id'])

    return jsonify({'success': True,
                    'new_question': question,
                    'building_classes': new_building_classes})