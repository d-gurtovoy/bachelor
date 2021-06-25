import json
import pickledb

#person_label = pickledb.load('personDB.db', False)
person_index = pickledb.load('person_index.db', False)

gt = json.load(open('wikidata_all.json','r'))
suffix = json.load(open('suffixe.json','r'))

correct = []
incorrect = []
none = []
total = 4799

for i in gt['results']['bindings']:
    item = {
    'street_label' : (i['streetLabel']['value']).replace('-',' '),
    'street_id' : (i['street']['value']).replace('http://www.wikidata.org/entity/',''),
    'street_gt' : (i['person']['value']).replace('http://www.wikidata.org/entity/','')
    }


    for s in suffix:
        if s in item['street_label']:
            query = item['street_label'].replace(s,'')
            break
        else:
            query = item['street_label']
    item['query'] = query

    try:
        result = person_index.get(query)
        if result[0][0] == item['street_gt']:
            correct.append(item)
        else:
            incorrect.append(item)
    except:
        none.append(item)

correct_list = json.dumps(correct, indent=4)
incorrect_list = json.dumps(incorrect, indent=4)
none_list = json.dumps(none, indent=4)

with open('naive_correct.json','w') as output_correct:
    output_correct.write(correct_list)

with open('naive_incorrect.json','w') as output_cinorrect:
    output_cinorrect.write(incorrect_list)

with open('naive_none.json','w') as output_none:
    output_none.write(none_list)

print(len(correct),len(incorrect),len(none))
