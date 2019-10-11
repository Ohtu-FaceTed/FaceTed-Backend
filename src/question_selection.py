import numpy as np
import src
from src.sessionManagement import users
from flask import session

def entropy(probabilities):
    '''Calculates entropy with given probabilities P(Y|X)'''
    H = 0
    for i in probabilities['posterior']:
        H += i * np.log(i)
    H = H*(-1)
    
    return H

def new_entropy(attribute):
    '''Calculates new entropy for question considering both answers'''
    prior = None
    try:
        #selects the previous probabilities as prior for calculating posterior
        prior = users[user]['probabilities'][-1]
    except:
        pass

    probabilites_yes = src.classifier.calculate_posterior(attribute, 'yes', prior)
    N0 = np.sum(probabilites_yes['posterior']) #Maybe this?
    probabilites_no = src.classifier.calculate_posterior(attribute, 'no', prior)
    N1 = np.sum(probabilites_no['posterior']) #Maybe this?

    return entropy(probabilites_yes) * N0 + entropy(probabilites_no) * N1

def best_questions():
    '''Sorts remaining questions from best to worst based on their entropies'''
    #Questions ordered from lowest to highest entropy
    entropies = []
    for i in src.building_data.attribute_name.keys():
        #Skip already asked questions
        if i in users[session['user']]['attributes']:
            continue
        H = new_entropy(i)
        entropies.append((i, H))

    entropies = sorted(entropies, key=lambda x: x[1])

    return entropies

def next_question():
    '''Returns best question to be asked next'''
    try:
        ident = best_questions()[0][0]
        return {"attribute_id": str(ident), "attribute_name": src.building_data.attribute_name[ident]}
    except IndexError:
        #All questions asked
        return {"attribute_id": '', "attribute_name": ''}
