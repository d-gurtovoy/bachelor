import pickledb as p
import json

personIndexDB = p.load('person_index.db',False)
personWiki = json.load(open('filtered_persons.json','r'))

lang = ['de','en','fr','ru']

for i in wikidata:
    for j in lang:
        key = i['label'][j]['value']
        value = i['id']
        try:
            personIndexDB.append(key,', '+value)
        except:
            personIndexDB.set(key,value)

personIndexDB.dump()
