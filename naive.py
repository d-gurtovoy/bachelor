import json
import pickledb

#person_label = pickledb.load('personDB.db', False)
#person_index = pickledb.load('person_index.db',False)
person_index = pickledb.load('person_index.db', False)

gt = json.load(open('wikidata_all.json','r'))
suffix = json.load(open('suffixe.json','r'))

res = []
correct = []
incorrect = []
none = []
total = 4799

for i in gt['results']['bindings']:
    street_label = i['streetLabel']['value']
    street_label = street_label.replace('-',' ')

    street_id = i['street']['value']
    street_id = street_id.replace('http://www.wikidata.org/entity/','')

    street_gt = i['person']['value']
    street_gt = street_gt.replace('http://www.wikidata.org/entity/','')

    for j in suffix:
        try:
            street_label = street_label.replace(j,'')
        except:
            pass
    try:
        result = person_index.get(street_label)
        if result[0][0] == street_gt:
            correct.append(street_label)
        else:
            incorrect.append(street_label)
    except:
        none.append(street_label)
'''
test = json.dumps(res, indent=4)

with open('test.json','w') as output:
    output.write(test)

'''

print(len(correct),len(incorrect),len(none))
