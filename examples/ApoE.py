from vmc.models import ObjectReference, Interval, Allele, Haplotype, Genotype

#                              rs7412 
#                              NC_000019.10:g.44908822
#                              C          T
#
# rs429358                 C   APOE-ε4    APOE-ε1
# NC_000019.10:g.44908684  T   APOE-ε3    APOE-ε2
# http://snpedia.com/index.php/APOE


sr = ObjectReference(namespace="NCBI", accession="NC_000019.10")

intervals = {
    "rs429358": Interval(44908683, 44908684),
    "rs7412": Interval(44908821, 44908822),
    }

alleles = {
    "rs429358T": Allele(sr, intervals["rs429358"], "T"),
    "rs429358C": Allele(sr, intervals["rs429358"], "C"),
    "rs7412T":   Allele(sr, intervals["rs7412"],   "T"),
    "rs7412C":   Allele(sr, intervals["rs7412"],   "C"),
    }

name_hap_map = {
    "ε1": Haplotype([alleles["rs429358C"], alleles["rs7412T"]]),
    "ε2": Haplotype([alleles["rs429358T"], alleles["rs7412T"]]),
    "ε3": Haplotype([alleles["rs429358T"], alleles["rs7412C"]]),
    "ε4": Haplotype([alleles["rs429358C"], alleles["rs7412C"]]),
    }
hap_name_map = {str(h.digest()): n for n, h in name_hap_map.items()}

haplotypes = list(name_hap_map.values())

genotypes = [Genotype([haplotypes[i], haplotypes[j]])
             for i in range(len(haplotypes))
             for j in range(i, len(haplotypes))]

