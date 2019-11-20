from flask import request, jsonify, session

from . import views as app
from src.sessionManagement import users
from src.models import db, Answer, AnswerQuestion, Attribute, BuildingClass, Session


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        content = request.get_json()
        # language = content['language'] FIXME: To be implemented
        class_id = content['class_id']
        #class_name = content['class_name']
        #response = content['response']
    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "class_id", "class_name" and "response" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "class_id", "class_name" and "response" in query'})
    else:
        if 'user' in session:
            user = users[session['user']]
            # Add the responses to the database. First find the appropriate rows
            # from attribute, answer, and session tables, then create the new
            # AnswerQuestion
            
            responses = []
            for one in user['user_responses']:
                responses.extend(one)
            for (attribute, resp) in responses:
                try:
                    db_attribute = Attribute.query.filter_by(
                        attribute_id=attribute).first()
                    db_answer = Answer.query.filter_by(value=resp).first()
                    db_session = Session.query.filter_by(
                        session_ident=session['user']).first()
                    db.session.add(AnswerQuestion(
                        db_attribute, db_answer, db_session))
                    db.session.commit()
                except AttributeError as e:
                    print(
                        'It seems one or more of attribute, answer or session have not been populated correctly:', e.args[0])
                    db.session.rollback()

            # save selected building class to database
            sess = Session.query.filter_by(
                session_ident=session['user']).first()
            selected_class = BuildingClass.query.filter_by(
                class_id=class_id).first()
            sess.selected_class = selected_class
            db.session.commit()

            # remove session and data related to it
            users.pop(session['user'], None)
            session.pop('user', None)

            return jsonify({'success': True})

        return jsonify({'success': False})
