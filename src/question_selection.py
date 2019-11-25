import numpy as np
import pandas as pd
import src
from .models import db, QuestionGroup, Attribute


def best_questions(prior, answered_questions):
    '''Returns attribute with lowest resultant entropy of posteriors'''

    # Find the attributes that have been asked and that can be asked
    # used_attributes = users[session['user']]['attributes']
    # Attribute.query.filter_by(attribute_id=x).first().grouping_id is not 'NaN'

    non_active = src.building_data._attributes.loc[src.building_data._attributes['active'] == False]
    na_attributes = non_active['attribute_id'].tolist()
    free_attributes = [x for x in src.building_data.observations.columns if x not in [
        'class_id', 'count'] and x not in answered_questions and x not in na_attributes]  # in na_attributes]

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

    # print(type(entropy[0]))

    return entropy


def next_question(prior, answered_questions):
    '''Returns best question to be asked next'''

    best = best_questions(prior, answered_questions)
    if best:
        ident = best[0][0]
        attribute = src.building_data.attribute[ident]

        # Checks if attribute is part of a group
        # if attribute.group_id is not 'NaN':
        if not pd.isnull(attribute['group_id']):
            groups = src.building_data.attribute_groups
            attributes = src.building_data._attributes
            group = groups.loc[groups['group_id'] == attribute['group_id']]
            selected = attributes.loc[attributes['group_id'].isin(
                group['group_id'])]
            new_attributes = []
            group_question = None

            for index, row in selected.iterrows():
                new_attributes.append({'attribute_id': row['attribute_id'],
                                       'attribute_name': row['attribute_name']})

            if len(group['group_question']) > 0:
                group_question = group['group_question'].values[0]

            group = {
                'type': 'multi',
                'attribute_question': group_question,
                'attributes': new_attributes
            }
            return group
        else:
            question = {
                'type': 'simple',
                'attribute_id': attribute['attribute_id'],
                'attribute_name': attribute['attribute_name'],
                'attribute_question': attribute['attribute_question']
            }
            return question
    else:
        # FIXME: Is this coherent with the front end functionality?
        # All questions asked
        return {'attribute_id': '', 'attribute_name': '', 'attribute_question': ''}
