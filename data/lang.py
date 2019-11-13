import pandas as pd
import json

df = pd.read_csv("attributes.csv")
print(df)
eka = "{"
toka = "}"
df["attribute_question"] = df["attribute_question"].apply(lambda x: f'{eka}"fi":"{x}", "sv":"[Svenska]{x}", "en":"[English]{x}"{toka}')
# print(df["attribute_question"])
d = [json.loads(x) for x in df["attribute_question"]]
# print(d)

tips = '{"fi":"", "se":"", "en":"" }'
df["attribute_tooltip"] = tips
# print(d)

df.to_csv("new.csv", sep=",")

df = pd.read_csv("new.csv", sep=",")
# print(df)
d = [json.loads(x) for x in df["attribute_question"]]
print(d)
