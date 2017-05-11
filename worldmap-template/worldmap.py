import json
import pandas as pd
import unicodedata

gdi = {}

df = pd.read_csv('../gender_development_mod.csv')
for i in range(len(df)):
    #print df.ix[i][1],
    #print df.ix[i][2]
    gdi[str.lower(df.ix[i][1])] = df.ix[i][0]

print('--------------------------------')
count = 0
json_data=open('data/world-topo-min.json').read()
data = json.loads(json_data)
for d in data['objects']['countries']['geometries']:
    #print d['properties']['name'],
    d['properties']['color'] = '#ff1300'#'#CCD5FF'
    title = d['properties']['name']
    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
    if str.lower(title) in gdi.keys():
        #print d['properties']['name']
        #count += 1
        d['properties']['rank'] = gdi[str.lower(title)]
        if gdi[str.lower(title)] <= 60:
            d['properties']['color'] = '#adfcad'#'#003399'
        elif gdi[str.lower(title)] <= 130:
            d['properties']['color'] = '#ffba00'#'#3377FF'
        elif gdi[str.lower(title)] > 130:
            d['properties']['color'] = '#ff7d73'#'#99BBFF'
    else:
        #print(d['properties']['name'])
        #print(str.lower(title))
        count += 1


with open("data/world-topo-min.json", "w") as jsonFile:
    json.dump(data, jsonFile)

print('--------------------------------')
print(count)