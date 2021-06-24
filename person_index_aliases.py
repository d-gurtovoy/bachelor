import pickledb as p
import json

personIndexDB = p.load('person_index.db',False)
personWiki = json.load(open('filtered_persons.json','r'))
#personWiki = json.load(open('mini_db.json','r'))

lang = ['de','en','fr','ru']

for i in personWiki:
    for j in lang:
        # Hole für jede Sprache das Label, die Id, und den Fundort
        try:
            for x in i['aliases'][j]:
                key=x['value']
                value = [[i['id'], ['alias_'+j]]]

                try:
                    test = personIndexDB.get(key)
                    qids = []
                    for k in test:
                        qids.append(k[0])
                        if k[0] == i['id']:
                            k[1].append('alias_'+j)
                    if i['id'] not in qids:
                        personIndexDB.append(key,value)
                except:
                    personIndexDB.set(key,value)
        except:
            continue

personIndexDB.dump()
