import src
import json
import numpy as np

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import request, jsonify, session
from . import views as app
from . import select_question_by_language, get_best_match_language
from ..models import db, Session


@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()
        language = content['language']

        browser_languages = request.accept_languages
        best_match_language = get_best_match_language(browser_languages)

        attribute_id = []
        response = []
        for resp in content['response']:
            attribute_id.append(resp['attribute_id'])
            # FIXME: remove the lists in tests
            if not isinstance(resp['response'], str):
                response.append(resp['response'][0])
            else:
                response.append(resp['response'])
        #print('answer(), attribute_id:', attribute_id)
        #print('answer(), response:', response)

    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "attribute_id", and "response" in query'})
    else:

        user = None
        prior = None

        if 'user' not in session or session['user'] not in users:
            ident = generate_id()
            session['user'] = ident
            users[ident] = {'user_responses': [], 'server_responses': []}
            # Add the session to the database
            db.session.add(Session(ident))
            db.session.commit()
            user = users[ident]
        else:
            user = users[session['user']]

        #Save user responses
        user['user_responses'].append(list(zip(attribute_id, response)))

        # selects the previous probabilities as prior for calculating posterior
        if len(user['server_responses']) > 1:
            prior = []
            for one in user['server_responses'][-1]['building_classes']:
                prior.append(one['score'])
            prior = np.array(prior)

        posterior = src.classifier.calculate_posterior(
            attribute_id, response, prior)
        new_building_classes = []

        for _, (class_id, score) in posterior.iterrows():
            new_building_classes.append({'class_id': class_id,
                                         'class_name': src.building_data.building_class_name[class_id],
                                         'score': score})

        asked_attributes = []
        for resp in user['user_responses']:
            for one in resp:
                asked_attributes.append(one[0])
        question = next_question(prior, asked_attributes)
        print(question)
        if question['type'] == 'multi':
            for attribute in question['attributes']:
                attribute['attribute_name'] = select_question_by_language(
                    attribute['attribute_name'], best_match_language)

        lang_parsed_question = select_question_by_language(
            question['attribute_question'], best_match_language)

        question['attribute_question'] = lang_parsed_question

        json = {
            'new_question': question,
            'building_classes': new_building_classes
        }
        # Save response
        user['server_responses'].append(json)
        json['success'] = True
        return jsonify(json)
