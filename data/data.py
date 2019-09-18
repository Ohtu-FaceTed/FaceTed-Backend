import xlrd

def attributes():
  data = xlrd.open_workbook("luokat_kaikki.xls")
  keys = data.sheet_by_name("avain")
  attributes = []
  for row in keys.get_rows():
    if row[0].ctype == 1:
      attributes.append({
        "attribute_fi": row[1].value.encode("utf-8"),
        "attribute_id": int(row[0].value)
      })
  return attributes