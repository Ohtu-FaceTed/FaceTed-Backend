from src import app

from src.question import next_question
from src.sessionManagement import users

import data.data as data
from flask import request, jsonify, session


@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()
        language = content['language']
        attribute_id = content['attribute_id']
        response = content['response']
    except TypeError as e:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    except KeyError as e:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    else:

        user = None
        prior = None
        question = ''

        if 'user' in session:
            # access users session data
            user = users[session['user']]

        #selects the previous probabilities as prior for calculating posterior
        if len(user['probabilities']) > 0:
            prior = user['probabilities'][-1]

        posterior = data.calculate_posterior(attribute_id, response, prior)
        probabilities = posterior['posterior']
        new_building_classes = []
        for _, (class_id, score) in posterior.iterrows():
            new_building_classes.append({'class_id': class_id,
                                         'class_name': data.building_classes[class_id],
                                         'score': score})

        #Selects a question only once during session
        while True:
            q = next_question()
            if q['attribute_name'] not in user['questions']:
                question = q
                break

        #Saves current state
        user['probabilities'].append(probabilities)
        user['answers'].append(response)
        user['questions'].append(question['attribute_name'])
        user['attributes'].append(question['attribute_id'])

        return jsonify({'success': True,
                        'new_question': question,
                        'building_classes': new_building_classes})
