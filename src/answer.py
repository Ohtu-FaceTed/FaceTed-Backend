import src
from src import app

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import request, jsonify, session


@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()
        # language = content['language'] FIXME: To be implemented
        attribute_id = content['attribute_id']
        response = content['response']
    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    else:

        user = None
        prior = None

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

        # selects the previous probabilities as prior for calculating posterior
        if len(user['probabilities']) > 0:
            prior = user['probabilities'][-1]

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
        user['answers'].append(response)
        question = next_question()
        user['questions'].append(question['attribute_name'])
        user['question_strings'].append(question['attribute_question'])
        user['attributes'].append(question['attribute_id'])

        return jsonify({'success': True,
                        'new_question': question,
                        'building_classes': new_building_classes})
