from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme
from qwikidata.claim import WikidataClaimGroup,WikidataClaim
import json

f = json.load(open('filtered_subprops.json','r'))

lang = ['de', 'en', 'fr', 'ru']

person_claims = [
'P735',  #given name
'P734',  #family name
'P106',  #occupation
'P742'  #pseudonym
]

street_claims = [
'P131',  #located in administrative territorial entity
'P625',  #coordinates
'P402',  #OSM-ID
'P138'  #named after
]

def is_person_or_street(entity):
    try:
        claim_group = entity.get_truthy_claim_group('P31')
        claim = claim_group[0]
        qid = claim.mainsnak.datavalue.value['id']
        if qid == 'Q5':
            return 'person'
        if qid == 'Q79007':
            return 'street'
    except:
        return False


def filtered_properties(entity_dict, is_type):
    item = {
        'type': entity_dict['type'],
        'id' : entity_dict['id'],
        'labels' : {
            },
        'descriptions' : {
        },
        'aliases' : {
        },
        'claims':{
        },
        'sitelinks' : {
        }
    }
    for i in lang:
        try:
            item['labels'][i] = entity_dict['labels'][i]
        except:
            pass

        try:
            item['descriptions'][i] = entity_dict['descriptions'][i]
        except:
            pass

        try:
            item['aliases'][i] = entity_dict['aliases'][i]
        except:
            pass

        try:
            item['sitelinks'][i] = entity_dict['sitelinks'][i+'wiki'],
        except:
            pass

    if is_type == 'person':
        #general claims
        for i in person_claims:
            try:
                item['claims'][i] = entity_dict['claims'][i]
            except:
                pass

    if is_type == 'street':
        for k in street_claims:
            try:
                item['claims'][k] = entity_dict['claims'][k]
            except:
                pass

    #location related claims
    for j in f:
        try:
            item['claims'][j] = entity_dict['claims'][j]
        except:
            pass

    return item

#test_ent = get_entity_dict_from_api('Q570116')  #Alexanderplatz
test_ent = get_entity_dict_from_api('Q98400')     #Douglas Adams
#test_ent = get_entity_dict_from_api('Q15649764')#Mozartstraße
test_dict = WikidataItem(test_ent)



x = is_person_or_street(test_dict)
if x:
    test = filtered_properties(test_ent,x)
    print(test['claims'].keys())
else:
    print('no')
