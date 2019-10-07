import src
from src import app

from src.question import next_question
from src.sessionManagement import users

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
        if 'user' in session:
            # access users session data
            if session['user'] not in users:
                ident = generate_id()
                session['user'] = ident
                users[ident] = {'probabilities': [], 'answers': []}


        posterior = src.classifier.calculate_posterior(attribute_id, response)
        new_building_classes = []
        for _, (class_id, score) in posterior.iterrows():
            new_building_classes.append({'class_id': class_id,
                                         'class_name': src.building_data.building_class_name[class_id],
                                         'score': score})

        return jsonify({'success': True,
                        'new_question': next_question(),
                        'building_classes': new_building_classes})
