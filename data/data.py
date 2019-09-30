import xlrd
import numpy as np
import pandas as pd

data = xlrd.open_workbook("data/luokat_kaikki.xls")

#returns dictionary made up from attribute code and name pairs
def get_attributes():
  '''Loads attribute_id to attribute_name mapping from file and returns them as dict'''
  keys = data.sheet_by_name("avain")
  attributes = {}
  for row in keys.get_rows():
    #ignore empty cells
    if row[0].ctype != 0:
      attributes[str(int(row[0].value))] = row[1].value
  return attributes

# Load attributes here, so we don't need to read from disk on every request
attributes = get_attributes()

def get_building_classes():
  '''Loads building class_id to class_name mapping from file and returns them as dict'''
  # Read data (FIXME: hardcoding of path)
  data = pd.read_csv('data/building_classes.csv', sep=',', dtype=str)

  # Transform into dictionary
  building_classes = {class_id:class_name for ind,(class_id,class_name) in data.iterrows()}

  return building_classes

# Load building_classes here, so we don't need to read from disk on every request
building_classes = get_building_classes()

def get_building_observations_numpy():
  '''Loads building "observations" from file and returns them as Numpy array'''
  test = data.sheet_by_name("testi")
  classes = []
  for row in test.get_rows():
    classes.append(np.array(list(map(lambda one: one.value, row))))
  classes[0][0] = 0
  classes = np.array(classes).astype(float)
  classes[0,0] = None
  return classes

def get_building_observations():
  '''Loads building "observations" from file and returns them as Pandas dataframe'''
  # Read data from file FIXME: hardcoded of paths
  df = pd.read_excel("data/luokat_kaikki.xls", dtype={'class_id': str})

  # Make sure the column names are strings
  df.columns = df.columns.astype(str)

  # Just take the main code for each class_id (ignore decimal part) 
  # FIXME: is this what the customer wants?
  df.class_id = df.class_id.apply(lambda x: x[:4])

  return df

# Load building_observations, so we don't need to read from disk on every request
building_observations = get_building_observations()

def get_conditional_probabilities():
  '''Calculates the conditional probability table from the building observations and returns them as a Pandas dataframe'''
  # Start with building_observations
  df = building_observations.copy()

  # Find attribute columns
  attribute_cols = df.columns[df.columns != 'class_id']

  # Convert the observation values into probabilities with Laplace smoothing
  df[attribute_cols] = (df[attribute_cols] + 1)/3 

  return df

# Calculate conditional probabilites here, so we don't need to do it on every request
conditional_probabilities = get_conditional_probabilities()

def calculate_posterior(attribute, value, prior=None, normalize=True):
  '''Calculates the posterior probability for each building class given attribute and value'''
  n_building_class = conditional_probabilities.shape[0]

  # Assume uniform prior if none is provided
  if prior is None:
    prior = np.ones(n_building_class)

  # Extract the likelihood from the conditional probability table
  if value == True:
    likelihood = conditional_probabilities[attribute]
  else:
    likelihood = 1-conditional_probabilities[attribute]

  # Calculate the posterior and normalize if requested
  posterior = prior * likelihood
  if normalize:
    posterior /= posterior.sum()

  # Create Pandas dataframe with building class and posterior
  df = pd.DataFrame({'class_id': conditional_probabilities['class_id'], 
                     'posterior': posterior})
  
  return df
