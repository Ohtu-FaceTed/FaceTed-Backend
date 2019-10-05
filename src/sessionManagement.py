import random
from flask import Flask, escape, request, jsonify, session
import string

# to store every users session data
users = {}

def generate_id():
    '''Composes 10 characters long string id chosen randomly from letters and numbers and yet checks if it's already in use'''
    while (True):
        id = ''.join(random.choice(string.ascii_letters + string.digits)
                     for i in range(10))
        if not id in users:
            return id