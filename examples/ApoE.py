#                              rs7412 
#                              NC_000019.10:g.44908822
#                              C          T
#
# rs429358                 C   APOE-ε4    APOE-ε1
# NC_000019.10:g.44908684  T   APOE-ε3    APOE-ε2
# http://snpedia.com/index.php/APOE

import json
import pprint

from vmc.richmodels import ObjectReference, Interval, Allele, Haplotype, Genotype
import vmc.codecs.json


sr = ObjectReference(namespace="NCBI", accession="NC_000019.10")

print(sr)


print("\nIntervals:")
intervals = {
    "rs429358": Interval(44908683, 44908684),
    "rs7412": Interval(44908821, 44908822),
    }
for k, o in intervals.items():
    print(k, o)


print("\nAlleles:")
alleles = {
    "rs429358T": Allele(sr, intervals["rs429358"], "T"),
    "rs429358C": Allele(sr, intervals["rs429358"], "C"),
    "rs7412T":   Allele(sr, intervals["rs7412"],   "T"),
    "rs7412C":   Allele(sr, intervals["rs7412"],   "C"),
    }
for k, o in alleles.items():
    print(k, o.digest, str(o))


print("\nHaplotypes:")
haplotypes = {
    "ε1": Haplotype([alleles["rs429358C"], alleles["rs7412T"]]),
    "ε2": Haplotype([alleles["rs429358T"], alleles["rs7412T"]]),
    "ε3": Haplotype([alleles["rs429358T"], alleles["rs7412C"]]),
    "ε4": Haplotype([alleles["rs429358C"], alleles["rs7412C"]]),
    }
for k, o in haplotypes.items():
    print(k, o.digest, o)


haplotype_names = {str(h.digest): n for n, h in haplotypes.items()}
print("\nHaplotype Names:")
pprint.pprint(haplotype_names)


print("\nGenotypes:")
genotypes = {
    "{}/{}".format(h1n, h2n): Genotype([h1, h2])
    for h1n, h1 in haplotypes.items()
    for h2n, h2 in haplotypes.items()
    }
for k, o in sorted(genotypes.items(), key=lambda kv: kv[0]):
    print(k, o.digest)




patient_data = {
    "sample-id": "e89c387a-b539-11e6-9d82-fb96077e5724",

    "vmc:alleles": alleles.values(),
    "vmc:haplotypes": haplotypes.values(),
    "vmc:genotypes": genotypes.values(),

    "haplotype_names": haplotype_names,

    "clinical significance": {
        "VH/q8_JMk85MxhmFXOAGYsf4aFoHuOyfAJE": "increased risk",
        }
    }

print(json.dumps(patient_data, indent=2, sort_keys=True,
                 cls=vmc.codecs.json.JSONEncoder))
