import xlrd
import numpy as np

data = xlrd.open_workbook("data/luokat_kaikki.xls")

def attributes():
  keys = data.sheet_by_name("avain")
  attributes = {}
  for row in keys.get_rows():
    if row[0].ctype != 0:
      attributes[str(row[0].value)] = row[1].value.encode("utf-8")
  return attributes

def test_data():
  test = data.sheet_by_name("testi")
  classes = []
  for row in test.get_rows():
    classes.append(np.array(map(lambda one: one.value, row)))
  return np.array(classes).astype(str)

