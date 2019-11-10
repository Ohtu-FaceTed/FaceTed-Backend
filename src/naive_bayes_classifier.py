import numpy as np
import pandas as pd


def calculate_conditional_probabilities(observations):
    '''Calculates the conditional probability table from the building observations and returns them as a Pandas dataframe'''
    # Start with building_observations
    df = observations.copy()

    # Find attribute columns
    attribute_cols = df.columns[(
        df.columns != 'class_id') & (df.columns != 'count')]

    # Convert the observation values into probabilities with Laplace smoothing
    df[attribute_cols] = (df[attribute_cols] + 1) / (df['count'][:, None] + 2)

    return df


class NaiveBayesClassifier:
    def __init__(self, observations):
        self.observations = observations
        self.conditional_probabilities = calculate_conditional_probabilities(
            observations)

    def calculate_posterior(self, attribute, value, prior=None, normalize=True):
        '''Calculates the posterior probability for each building class given attribute and value'''

        prior_probability = prior
        posterior = None
        # Assume uniform prior if none is provided
        if prior_probability is None:
            prior_probability = np.ones(self.observations.shape[0])
        print(value)
        print(attribute)

        # Extract the likelihood from the conditional probability table
        for (val, attr) in zip(value, attribute): 
            if val == 'yes':
                likelihood = self.conditional_probabilities[attr]
            elif val == 'no':
                likelihood = 1 - self.conditional_probabilities[attr]
            else:
                likelihood = 1

            # Calculate the posterior and normalize if requested
            posterior = prior_probability * likelihood

            if normalize:
                posterior /= posterior.sum()
            prior_probability = posterior

        # Create Pandas dataframe with building class and posterior
        df = pd.DataFrame({'class_id': self.conditional_probabilities.class_id,
                           'posterior': posterior})
        return df
