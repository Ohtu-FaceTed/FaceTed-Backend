from src import app
from src import session
from src.session import generate_id, users

import argparse
import random
import data.data as data
from flask import Flask, escape, request, jsonify, session
import string


# could be moved to its own module
def next_question():
    id = random.choice(list(data.attributes.keys()))
    return {"attribute_id": str(id), "attribute_name": data.attributes.get(id)}


@app.route('/question', methods=['GET'])
def question():
    # remove users previous state
    if 'user' in session:
        users.pop(session['user'], None)

    id = generate_id()
    session['user'] = id
    users[id] = {'probabilities': [], 'answers': []}
    return jsonify(next_question())
