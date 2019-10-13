import random
# from flask import session // Will this ever be used here?
import string

# to store every users session data
users = {}


def generate_id():
    '''Composes 10 characters long string id chosen randomly from letters and numbers and yet checks if it's already in use'''
    while (True):
        ident = ''.join(random.choice(string.ascii_letters + string.digits)
                        for i in range(10))
        if not ident in users:
            return ident
