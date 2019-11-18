import numpy as np
import pandas as pd

# The observations dataframe should have at least the following columns:
#   class_id: same as building_classes class_id (string, unique)
#   count: number of observations of this class (int, positive)
#   [attribute]: number of observations of this attribute for a given class_id (integer)
DEFAULT_OBSERVATIONS = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                     'count': [1, 1, 1],
                                     '1': [1, 1, 1],
                                     '101': [1, 0, 1],
                                     '102': [0, 1, 0]})


def load_observations(observation_file):
    '''Attempts to load buiding-attribute observation data from file into Pandas dataframe'''
    df = pd.read_csv(observation_file, dtype={'class_id': str})

    # Check that the required fields are present
    for required_field in ['class_id', 'count']:
        if required_field not in df:
            raise ValueError(
                f"The observations data ({observation_file}) does not contain a '{required_field}' column!")

    # Check that we have at least one "attribute" column in addition to
    # class_id and count
    if len(df.columns) < 3:
        raise ValueError(
            f"The observation data ({observation_file}) does not contain any attribute columns!")

    # Check that there is at least one row of data
    if len(df.index) < 1:
        raise ValueError(
            f"The observation data ({observation_file}) does not contain any rows!")

    # Check counts are positive integers
    if not np.equal(np.mod(df['count'], 1), 0).all or (df['count'] < 1).any():
        raise ValueError(
            "Found 'count' values in observation data that are not positive integers")

    # Ensure that the column labels are interpreted as strings
    df.columns = df.columns.astype(str)

    return df


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
    def __init__(self, observation_file):
        self.observation_file = observation_file
        try:
            self.observations = load_observations(observation_file)
        except ValueError as error:
            print(
                f'Unable to load observations ({observation_file}): {error.args[0]}')
            self.observations = DEFAULT_OBSERVATIONS
        self.conditional_probabilities = calculate_conditional_probabilities(
            self.observations)

    def calculate_posterior(self, attribute, value, prior=None, normalize=True):
        '''Calculates the posterior probability for each building class given attribute and value'''

        prior_probability = prior
        posterior = None
        # Assume uniform prior if none is provided
        if prior_probability is None:
            prior_probability = np.ones(self.observations.shape[0])

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
