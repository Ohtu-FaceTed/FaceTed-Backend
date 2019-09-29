import xlrd
import numpy as np
import pandas as pd

data = xlrd.open_workbook("data/luokat_kaikki.xls")

#returns dictionary made up from attribute code and name pairs
def get_attributes():
  keys = data.sheet_by_name("avain")
  attributes = {}
  for row in keys.get_rows():
    #ignore empty cells
    if row[0].ctype != 0:
      attributes[str(int(row[0].value))] = row[1].value
  return attributes

attributes = get_attributes()

def get_building_classes():
  # Read data (FIXME: hardcoding of path)
  data = pd.read_csv('data/building_classes.csv', sep=',', dtype=str)

  # Transform into dictionary
  building_classes = {class_id:class_name for ind,(class_id,class_name) in data.iterrows()}

  return building_classes

building_classes = get_building_classes()

#returns two-dimensional numpy array of building class data
def get_building_observations():
  test = data.sheet_by_name("testi")
  classes = []
  for row in test.get_rows():
    classes.append(np.array(list(map(lambda one: one.value, row))))
  classes[0][0] = 0
  classes = np.array(classes).astype(float)
  classes[0,0] = None
  return classes

building_observations = get_building_observations()

def get_conditional_probabilities():  
  # Extract column names and convert them to strings
  columns = building_observations[0,1:].astype(int).astype(str)

  # Extract "observations" and convert them to "probabilities"
  observations = building_observations[1:,1:]
  probabilities = (observations + 1)/3 # Laplace smoothing

  # Create a Pandas dataframe to allow mixed datatypes and keep column names
  df = pd.DataFrame(data=probabilities, columns=columns)

  # Add building class column, yes the transformation is a bit gnarly
  building_class = [f'{int(x):04d}' if x%1==0. else f'{x:06.1f}' for x in building_observations[1:,0]]
  df.insert(0, column='building_class', value=building_class)

  return df

conditional_probabilities = get_conditional_probabilities()

def calculate_posterior(attribute, value, prior=None, normalize=True):
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
  df = pd.DataFrame({'building_class': conditional_probabilities['building_class'], 
                     'posterior': posterior})

  return df
