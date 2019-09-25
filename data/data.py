import xlrd
import numpy as np
import pandas as pd

data = xlrd.open_workbook("data/luokat_kaikki.xls")

#returns dictionary made up from attribute code and name pairs
def attributes():
  keys = data.sheet_by_name("avain")
  attributes = {}
  for row in keys.get_rows():
    #ignore empty cells
    if row[0].ctype != 0:
      attributes[float(row[0].value)] = row[1].value
  return attributes

#returns two-dimensional numpy array of building class data
def building_classes_numpy():
  test = data.sheet_by_name("testi")
  classes = []
  for row in test.get_rows():
    classes.append(np.array(list(map(lambda one: one.value, row))))
  classes[0][0] = 0
  classes = np.array(classes).astype(float)
  classes[0,0] = None
  return classes

#returns building class data in pandas dataframe
def building_classes_dataframe():
  df = pd.read_excel("data/luokat_kaikki.xls", dtype={'Index': str})
  df = df.set_index('Index')
  df.columns = df.columns.astype(str)
  df = df.astype(float)
  return df
