import pandas as pd
import json

# WARNING MIGHT CHANGE INTEGERS IN CSV TO FLOATS FOR NO APPARENT REASON

#original csv to be edited
df = pd.read_csv("original.csv")

#actual edit. current setup makes columns json formatted for language support
eka = "{"
toka = "}"
df["attribute_name"] = df["attribute_name"].apply(lambda x: f'{eka}"fi":"{x}", "sv":"[Svenska]{x}", "en":"[English]{x}"{toka}')
d = [json.loads(x) for x in df["attribute_name"]]

#creates new file, edit first attribute to choose new file name
df.to_csv("attributes.csv", sep="," , index = False)

#prints content of new file
df = pd.read_csv("attributes.csv", sep="," , index = False)
print(df)
d = [json.loads(x) for x in df["attribute_name"]]
print(d)