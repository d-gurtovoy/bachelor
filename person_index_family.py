import pickledb as p
import json

personIndexDB = p.load('person_index.db',False)
personWiki = json.load(open('filtered_persons.json','r'))
#personWiki = json.load(open('mini_db.json','r'))

lang = ['de','en','fr','ru']

for i in personWiki:
    for j in lang:
        try:
            full_name = (i['labels'][j]['value']).split()
            key = full_name[-1]
            value = [[i['id'], ['family_'+j]]]
        except:
            continue

        try:
            test = personIndexDB.get(key)
            qids = []
            for k in test:
                qids.append(k[0])
                if k[0] == i['id']:
                    k[1].append('family_'+j)
            if i['id'] not in qids:
                personIndexDB.append(key,value)
        except:
            personIndexDB.set(key,value)

print(personIndexDB.get('Beethoven'))

#personIndexDB.dump()
