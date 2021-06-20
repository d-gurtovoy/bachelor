import pickledb as p
import json

personIndexDB = p.load('person_index.db',False)
personWiki = json.load(open('filtered_persons.json','r'))

lang = ['de','en','fr','ru']


for i in personWiki:
    for j in lang:
        try:
            key = i['labels'][j]['value']
            value = i['id']
        except:
            pass
        try:
            ids = personIndexDB.get(key)
            if value in ids:
                pass
            else:
                personIndexDB.append(key,', '+value)
        except:
            personIndexDB.set(key,value)

personIndexDB.dump()
