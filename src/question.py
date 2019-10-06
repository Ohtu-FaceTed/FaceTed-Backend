from src import app
from src.sessionManagement import generate_id, users

import random
import data.data as data
from flask import jsonify, session


# could be moved to its own module
def next_question():
    ident = random.choice(list(data.attributes.keys()))
    return {"attribute_id": str(ident), "attribute_name": data.attributes.get(ident)}


@app.route('/question', methods=['GET'])
def question():
    # remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    ident = generate_id()
    session['user'] = ident
    users[ident] = {'probabilities': [], 'answers': []}
    return jsonify(next_question())
