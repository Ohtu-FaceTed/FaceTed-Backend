import numpy as np
import src


def best_questions(prior, answered_questions):
    '''Returns attribute with lowest resultant entropy of posteriors'''

    # Find the attributes that have been asked and that can be asked
    # used_attributes = users[session['user']]['attributes']
    free_attributes = [x for x in src.building_data.observations.columns if x not in [
        'class_id', 'count'] and x not in answered_questions]

    # Get the conditional probability table and the prior
    cond_p = src.classifier.conditional_probabilities[free_attributes]
    prior = prior if prior is not None else np.ones(
        cond_p.shape[0]) / cond_p.shape[0]
    # prior = np.ones(cond_p.shape[0]) / cond_p.shape[0] if not users[session['user']
    #                                                                ]['probabilities'] else users[session['user']]['probabilities'][-1]

    # Calculate and normalize posteriors for yes and no answers
    p_yes = cond_p * prior[:, None]
    p_yes /= p_yes.sum(axis=0)
    p_no = (1 - cond_p) * prior[:, None]
    p_no /= p_no.sum(axis=0)

    # Calculate entropy
    entropy = -(p_yes * np.log(p_yes)).sum(axis=0) - \
        (p_no * np.log(p_no)).sum(axis=0)
    entropy = entropy.sort_values()
    entropy = [(i, x) for i, x in zip(entropy.index, entropy)]

    return entropy


def next_question(prior, answered_questions):
    '''Returns best question to be asked next'''
    best = best_questions(prior, answered_questions)
    if best:
        ident = best[0][0]
        return src.building_data.attribute[ident]
    else:
        # All questions asked
        return {"attribute_id": '', "attribute_name": '', 'attribute_question': ''}
