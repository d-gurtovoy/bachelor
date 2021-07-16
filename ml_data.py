import json
import pickledb as p
import pandas as pd
import time

gt = json.load(open('wikidata_all.json','r'))
suffix = json.load(open('suffixe.json','r'))
links = pd.read_csv('link_counts_wikidata.tsv', sep='\t', index_col='Q64')
person_indexDB = p.load('person_index.db',False)
person_familyDB = p.load('person_index_family.db',False)
personDB = p.load('personDB.db',False)
#df = pd.read_csv('test.csv',index_col=0)

header = {'street':[],'candidate':[],'full_name':[],'first_name':[],
    'last_name':[],'alias':[],'popularity':[],'politiker':[],'schriftsteller':[],
    'hochschullehrer':[],'dichter':[],'philosoph':[],'correct_entity':[]}
df = pd.DataFrame(header)

for t,i in enumerate(gt['results']['bindings']):
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

# Popularity Ranking
    result = person_index.get(query)
    if result == False:
        result = person_index_family.get(query)
    if result == False:
        continue

    for r in result:
        if 'alias_de' in r[1] or 'alias_en' in r[1]:
            alias = 1
        else:
            alias = 0
        if 'family_de' in r[1] or 'family_en' in r[1]:
            last_name = 1
        else:
            last_name = 0
        # get link count per candidate
        try:
            qid = r[0]
            count = int(links.loc[qid][1])
        except:
            count = ''

        # get occupation and mark is accordingly
        ent = personDB.get(r)

        # mark the correct candidate accordingly
        if r == item['street_gt']:
            correct = 1
        else:
            correct = 0

        row = [{
        'street' : item['street_id'],
        'candidate': r,
        'full_name': full_name,
        'first_name':first_name,
        'last_name': last_name,
        'alias': alias,
        'popularity': count,
        'politiker': politiker,
        'schriftsteller': schriftsteller,
        'hochschullehrer': hochschullehrer,
        'dichter':dichter,
        'philosoph':philosoph,
        'correct_entity':correct
        }]
        df = df.append(row,ignore_index=True,sort=False)

    if t>10:
        break

with open('test.csv','w') as output:
    df.to_csv(output,header=False)
