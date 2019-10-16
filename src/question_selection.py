import numpy as np
import src
from src.sessionManagement import users
from flask import session


def entropy(probabilities):
    '''Calculates entropy with given probabilities P(Y|X)'''
    H = 0
    for i in probabilities['posterior']:
        H += i * np.log(i)
    H = H * (-1)

    return H


def new_entropy(attribute):
    '''Calculates new entropy for question considering both answers'''
    # selects the previous probabilities as prior for calculating posterior
    prior = None
    if users[session['user']]['probabilities']:
        prior = users[session['user']]['probabilities'][-1]

    probabilites_yes = src.classifier.calculate_posterior(
        attribute, 'yes', prior)
    N0 = np.sum(probabilites_yes['posterior'])  # Maybe this?
    probabilites_no = src.classifier.calculate_posterior(
        attribute, 'no', prior)
    N1 = np.sum(probabilites_no['posterior'])  # Maybe this?

    return entropy(probabilites_yes) * N0 + entropy(probabilites_no) * N1

def best_questions_old():
    '''Sorts remaining questions from best to worst based on their entropies'''
    # Questions ordered from lowest to highest entropy
    entropies = []
    for i in src.building_data.attribute_name.keys():
        # Skip already asked questions
        if i in users[session['user']]['attributes']:
            continue
        H = new_entropy(i)
        entropies.append((i, H))

    entropies = sorted(entropies, key=lambda x: x[1])

    return entropies

def best_questions():
    '''Returns attribute with lowest resultant entropy of posteriors'''

    # Find the attributes that have been asked and that can be asked
    used_attributes = users[session['user']]['attributes']
    free_attributes = [x for x in src.building_data.observations.columns if x not in ['class_id', 'count'] and x not in used_attributes]

    # Get the conditional probability table and the prior
    cond_p = src.classifier.conditional_probabilities[free_attributes]
    prior = np.ones(cond_p.shape[0])/cond_p.shape[0] if not users[session['user']]['probabilities'] else users[session['user']]['probabilities'][-1]

    # Calculate and normalize posteriors for yes and no answers
    p_yes = cond_p*prior[:,None]
    p_yes /= p_yes.sum(axis=0)
    p_no = (1-cond_p)*prior[:,None]
    p_no /= p_no.sum(axis=0)

    # Calculate entropy
    entropy = -(p_yes*np.log(p_yes)).sum(axis=0) - (p_no*np.log(p_no)).sum(axis=0)
    entropy = entropy.sort_values()
    entropy = [(i,x) for i,x in zip(entropy.index, entropy)]

    return entropy

def next_question():
    '''Returns best question to be asked next'''
    best = best_questions()
    if best:
        ident = best[0][0]
        return {"attribute_id": ident, "attribute_name": src.building_data.attribute_name[ident]}
    else:
        # All questions asked
        return {"attribute_id": '', "attribute_name": ''}
