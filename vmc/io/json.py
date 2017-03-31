import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'as_dict'):
            return obj.as_dict()
        return json.JSONEncoder.default(self, obj)


def to_json(self):
    doc = {
        "vmc": {
            "version": 1,
        },
        "alleles": [a.as_dict() for a in self.alleles],
        "haplotypes": [],
        "genotypes": [],
        "identifier_id_map": {},
        "relationships": {
            "classes": {},
            "relations": {
                "<class>": []
                }
        },
    }
    return json.dumps(doc, indent=2, sort_keys=True,
                      cls=vmc.codecs.json.JSONEncoder,
                      ensure_ascii=False)
