import json
import pickledb
import pandas as pd
import os

# Benötigte Dateien
#person_label = pickledb.load('personDB.db', False)
#person_index = pickledb.load('person_index.db', False)
#person_index_family = pickledb.load('person_index_family.db', False)
#links = pd.read_csv('link_counts_wikidata.tsv', sep='\t')
gt = json.load(open('wikidata_all.json','r'))
suffix = json.load(open('suffixe.json','r'))

# Liste für Ergebnisse
correct = []
incorrect = []
none = []
total = 4799

for i in gt['results']['bindings']:
# Für jede Straße in der Ground Truth ein Dictionary anlegen
    item = {
    'street_label' : (i['streetLabel']['value']).replace('-',' '),
    'street_id' : (i['street']['value']).replace('http://www.wikidata.org/entity/',''),
    'street_gt' : (i['person']['value']).replace('http://www.wikidata.org/entity/','')
    }

# Suffixe filtern und als Query abspeichern
    for s in suffix:
        if s in item['street_label']:
            query = item['street_label'].replace(s,'').rstrip()
            break
        else:
            query = item['street_label']
    item['query'] = query

# Popularity Ranking
    try:
        query = query.replace(' ','_')
        proc = os.popen('grep '+query+' link_counts_wikidata.tsv')
        lines = proc.read(50)
        proc.close()
        if lines[0] == item['street_gt']:
            correct.append(query)
        else:
            incorrect.append(query)
    except:
        none.append(none)

# Write results
correct_list = json.dumps(correct, indent=4)
incorrect_list = json.dumps(incorrect, indent=4)
none_list = json.dumps(none, indent=4)

with open('popularity_correct01.json','w') as output_correct:
    output_correct.write(correct_list)

with open('popularity_incorrect01.json','w') as output_inorrect:
    output_inorrect.write(incorrect_list)

with open('popularity_none01.json','w') as output_none:
    output_none.write(none_list)


# Ergebnisse berechnen
print(len(correct),len(incorrect),len(none))
precision = len(correct)/(len(correct)+len(incorrect))
recall = len(correct)/total
f1 = (2*precision*recall)/(precision+recall)
print(('precision: {}'.format(precision)))
print(('recall: {}'.format(recall)))
print(('f1-score: {}'.format(f1)))
