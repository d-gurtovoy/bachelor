import time

from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
from qwiki import filtered_entities, is_human
import json

# create an instance of WikidataJsonDump
wjd_dump_path = "wikidata-20210517-all.json.bz2"
wjd = WikidataJsonDump(wjd_dump_path)

# create an iterable of WikidataItem representing politicians
results = []
t1 = time.time()
for ii, entity_dict in enumerate(wjd):

    if entity_dict["type"] == "item":
        try:
            entity = WikidataItem(entity_dict)
            if is_human(entity):
                x = filtered_entities(entity_dict)
                res = type_to_entity_class[x](entity_dict)
                results.append(res)
        except:
            continue
    if ii % 1000 == 0:
        t2 = time.time()
        dt = t2 - t1
        print(
            "found {} humans among {} entities [entities/s: {:.2f}]".format(
                len(results), ii, ii / dt
            )
        )

    if ii > 10:
        break

# write the iterable of WikidataItem to disk as JSON
out_fname = "filtered_entities.json"
dump_entities_to_json(results, out_fname)
wjd_filtered = WikidataJsonDump(out_fname)

# load filtered entities and create instances of WikidataItem
for ii, entity_dict in enumerate(wjd_filtered):
    item = WikidataItem(entity_dict)
