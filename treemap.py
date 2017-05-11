import json
import pandas as pd
import unicodedata
import sys

wage_diff = {}
regions = {}
df = pd.read_csv('gender_development_mod.csv')
max = 0
for i in range(len(df)):
    wage_diff[str.lower(df.ix[i][1])] = df.ix[i][12] - df.ix[i][11]
    if df.ix[i][12] - df.ix[i][11] > max:
        max = df.ix[i][12] - df.ix[i][11]
print max
json_data=open('countries.json').read()
data = json.loads(json_data)

for d in data:
    regions[d['region']] = 1
    regions[d['subregion']] = 1
    title = d['key']
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
    if str.lower(title) in wage_diff.keys():
        d['value'] = wage_diff[str.lower(title)]
    else:
        d['value'] = -1
        #print d['key']

with open("countries.json", "w") as jsonFile:
    json.dump(data, jsonFile)

s = set(regions.keys())
for a in s:
    print "\"" + a + "\",",
    #print a,