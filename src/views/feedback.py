from flask import request, jsonify, session

from . import views as app
from src.sessionManagement import users

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        content = request.get_json()
        # language = content['language'] FIXME: To be implemented
        class_id = content['class_id']
        class_name = content['class_name']
        response = content['response']
    except TypeError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "class_id", "class_name" and "response" in query'})
    except KeyError:
        return jsonify({'success': False,
                        'message': 'Please supply "language", "class_id", "class_name" and "response" in query'})
    else:
        if 'user' in session:
            #TODO: save answer vector with building class to database

            #remove session and data related to it
            users.pop(session['user'], None)
            session.pop('user', None)
            
            return jsonify({'success': True})

        return jsonify({'success': False})
