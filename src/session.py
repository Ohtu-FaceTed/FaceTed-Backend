import argparse
import random
import data.data as data
from flask import Flask, escape, request, jsonify, session
from flask_cors import CORS
import string
from src import app

# to store every users session data
users = {}

def generate_id():
    '''Composes 10 characters long string id chosen randomly from letters and numbers and yet checks if it's already in use'''
    while (True):
        id = ''.join(random.choice(string.ascii_letters + string.digits)
                     for i in range(10))
        if not id in users:
            return id