import time

from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
import json
import qwiki

P_IS_INSTANCE_OF = "P31"
Q_HUMAN = "Q5"



def is_human(item: WikidataItem, truthy: bool = True) -> bool:
    """Return True if the Wikidata Item is a human."""
    if truthy:
        claim_group = item.get_truthy_claim_group(P_IS_INSTANCE_OF)
    else:
        claim_group = item.get_claim_group(P_IS_INSTANCE_OF)

    human_qids = [
        claim.mainsnak.datavalue.value["id"]
        for claim in claim_group
        if claim.mainsnak.snaktype == "value"
    ]
    return Q_HUMAN in human_qids


# create an instance of WikidataJsonDump
wjd_dump_path = "wikidata-20210517-all.json.bz2"
wjd = WikidataJsonDump(wjd_dump_path)

# create an iterable of WikidataItem representing politicians
results = []
t1 = time.time()
for ii, entity_dict in enumerate(wjd):

    if entity_dict["type"] == "item":
        entity = WikidataItem(entity_dict)
        if is_human(entity):
            filtered_entity = filtered_entities(entity_dict)
            results.append(filtered_entity)

    if ii % 1000 == 0:
        t2 = time.time()
        dt = t2 - t1
        print(
            "found {} humans among {} entities [entities/s: {:.2f}]".format(
                len(results), ii, ii / dt
            )
        )

    if ii > 10000:
        break

# write the iterable of WikidataItem to disk as JSON
out_fname = "filtered_entities.json"
dump_entities_to_json(results, out_fname)
wjd_filtered = WikidataJsonDump(out_fname)

# load filtered entities and create instances of WikidataItem
for ii, entity_dict in enumerate(wjd_filtered):
    item = WikidataItem(entity_dict)
