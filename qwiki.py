from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme
from qwikidata.claim import WikidataClaimGroup,WikidataClaim
import json

f = json.load(open('filtered_subprops.json','r'))

# This is fine for small queries, for bigger queries use JSONDump
#create an instance of an entity item
entity_dict = get_entity_dict_from_api('Q76')
entity = WikidataItem(entity_dict)

# get claim 'educated at'
# use 'truthy' claims to get the statements that have the best rank for a given property (preferred)
#claim_groups = entity.get_truthy_claim_groups()
#p69_claim_group = claim_groups['P551']

#p69_claim_group = entity.get_truthy_claim_group('P69')

# Extract id from claim and turn into a WikidataItem
#claim = p69_claim_group[0]
#qid = claim.mainsnak.datavalue.value['id']
#entity = WikidataItem(get_entity_dict_from_api(qid))

def filtered_entities(entity_dict):
    if entity_dict['sitelinks']['dewiki']:
        item = {
            'pageid' : entity_dict['pageid'],
            'ns' : entity_dict['ns'],
            'title' : entity_dict['title'],
            'lastrevid' : entity_dict['lastrevid'],
            'modified' : entity_dict['modified'],
            'type': entity_dict['type'],
            'id' : entity_dict['id'],
            'labels' : {
                'de' : entity_dict['labels']['de']
                },
            'descriptions' : {
            },
            'aliases' : {
            },
            'claims':{
            },
            'sitelinks' : {
                'dewiki' : entity_dict['sitelinks']['dewiki'],
            }
        }
        try:
            item['aliases']['de'] = entity_dict['aliases']['de']
            item['descriptions']['de'] =  entity_dict['descriptions']['de']
        except:
            pass

    if 'enwiki' in entity_dict['sitelinks']:
        try:
            item['labels']['en'] = entity_dict['labels']['en']
            item['descriptions']['en'] = entity_dict['descriptions']['en']
            item['aliases']['en'] = entity_dict['aliases']['en']
            item['sitelinks']['enwiki'] = entity_dict['sitelinks']['enwiki']
        except:
            pass

    if 'frwiki' in entity_dict['sitelinks']:
        try:
            item['labels']['fr'] = entity_dict['labels']['fr']
            item['descriptions']['fr'] = entity_dict['descriptions']['fr']
            item['aliases']['ru'] = entity_dict['aliases']['ru']
            item['sitelinks']['ruwiki'] = entity_dict['sitelinks']['ruwiki']
        except:
            pass

    if 'ruwiki' in entity_dict['sitelinks']:
        try:
            item['labels']['ru'] = entity_dict['labels']['ru']
            item['descriptions']['ru'] = entity_dict['descriptions']['ru']
            item['aliases']['ru'] = entity_dict['aliases']['ru']
            item['sitelinks']['ruwiki'] = entity_dict['sitelinks']['ruwiki']
        except:
            pass

    # general claims
    try:
        item['claims']['P106'] = entity_dict['claims']['P106']  #occupation
        item['claims']['P735'] = entity_dict['claims']['P735']  #given name
        item['claims']['P734'] = entity_dict['claims']['P734']  #family name
        item['claims']['P742'] = entity_dict['claims']['P742']  #pseudonym
    except:
        pass

    # location claims
    for i in f:
        try:
            item['claims'][i] = entity_dict['claims'][i]
        except:
            pass
    return item
