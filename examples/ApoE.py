#                              rs7412 
#                              NC_000019.10:g.44908822
#                              C          T
#
# rs429358                 C   APOE-ε4    APOE-ε1
# NC_000019.10:g.44908684  T   APOE-ε3    APOE-ε2
# http://snpedia.com/index.php/APOE

import json

from vmc.models import ObjectReference, Interval, Allele, Haplotype, Genotype
import vmc.codecs.json


sr = ObjectReference(namespace="NCBI", accession="NC_000019.10")

print(sr)

intervals = {
    "rs429358": Interval(44908683, 44908684),
    "rs7412": Interval(44908821, 44908822),
    }

print("\nIntervals:")
for k, o in intervals.items():
    print(k, o)


alleles = {
    "rs429358T": Allele(sr, intervals["rs429358"], "T"),
    "rs429358C": Allele(sr, intervals["rs429358"], "C"),
    "rs7412T":   Allele(sr, intervals["rs7412"],   "T"),
    "rs7412C":   Allele(sr, intervals["rs7412"],   "C"),
    }

print("\nAlleles:")
for k, o in alleles.items():
    print(k, o.digest, str(o))


name_hap_map = {
    "ε1": Haplotype([alleles["rs429358C"], alleles["rs7412T"]]),
    "ε2": Haplotype([alleles["rs429358T"], alleles["rs7412T"]]),
    "ε3": Haplotype([alleles["rs429358T"], alleles["rs7412C"]]),
    "ε4": Haplotype([alleles["rs429358C"], alleles["rs7412C"]]),
    }
hap_name_map = {str(h.digest): n for n, h in name_hap_map.items()}

print("\nHaplotypes:")
for k, o in name_hap_map.items():
    print(k, o.digest, o)

haplotypes = list(name_hap_map.values())
genotypes = [Genotype([haplotypes[i], haplotypes[j]])
             for i in range(len(haplotypes))
             for j in range(i, len(haplotypes))]

print("\nGenotypes:")
for o in genotypes:
    print(o.digest, o)



patient_data = {
    "sample-id": "e89c387a-b539-11e6-9d82-fb96077e5724",

    "vmc:alleles": alleles,
    "vmc:haplotypes": haplotypes,
    "vmc:genotypes": genotypes,

    "haplotype_names": hap_name_map,

    "clinical significance": {
        "VH/q8_JMk85MxhmFXOAGYsf4aFoHuOyfAJE": "increased risk",
        }
    }

print(json.dumps(patient_data, indent=2, sort_keys=True,
                 cls=vmc.codecs.json.JSONEncoder))
