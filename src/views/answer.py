import src

from src.question_selection import next_question
from src.sessionManagement import users, generate_id

from flask import request, jsonify, session
from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, Session


@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()
        # language = content['language'] FIXME: To be implemented
        attribute_id = []
        response = []
        for resp in content['response']:
            attribute_id.append(resp['attribute_id'])
            response.append(resp['response'])
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
                users[ident] = {'type': [], 'probabilities': [], 'answers': [], 
                                'attributes': [], 'multi_attributes': [], 'question_strings': []}
                # Add the session to the database
                db.session.add(Session(ident))
                db.session.commit()
                user = users[ident]

        # Add the response to the database. First find the appropriate rows 
        # from attribute, answer, and session tables, then create the new 
        # AnswerQuestion
        for (attribute, resp) in zip(attribute_id, response): 
            try:
                db_attribute = Attribute.query.filter_by(attribute_id=attribute).first()
                db_answer = Answer.query.filter_by(value=resp).first()
                db_session = Session.query.filter_by(session_ident=session['user']).first()
                db.session.add(AnswerQuestion(db_attribute, db_answer, db_session))
                db.session.commit()
            except AttributeError as e:
                print('It seems one or more of attribute, answer or session have not been populated correctly:', e.args[0])
                db.session.rollback()

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
        db_session = Session.query.filter_by(session_ident=session['user']).first()
        answered = [question.attribute_id for question in db_session.answered_questions]
        question = next_question(user['probabilities'][-1], answered)
        if question['type'] == 'multi':
            user['type'].append('multi')
            user['multi_attributes'].append(question['attributes'])
        else:
            user['type'].append('simple')
            user['attributes'].append(question['attribute_id']) 
        user['question_strings'].append(question['attribute_question'])     
        user['answers'].append(answer)   

        return jsonify({'success': True,
                        'new_question': question,
                        'building_classes': new_building_classes})
