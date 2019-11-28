import random
from flask import session
import string
from .models import db, Session

# to store every users session data
users = {}


def generate_id():
    '''Composes 10 characters long string id chosen randomly from letters and numbers and yet checks if it's already in use'''
    while (True):
        ident = ''.join(random.choice(string.ascii_letters + string.digits)
                        for i in range(10))
        if not ident in users:
            return ident

def create_session():
    '''Creates and saves new session for user and returns session id'''
    ident = generate_id()
    session['user'] = ident
    users[ident] = {'user_responses': [], 'server_responses': []}
    # Add the session to the database
    db.session.add(Session(ident))
    db.session.commit()
    return ident
