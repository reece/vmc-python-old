from vmc.models import ObjectReference, Interval, Allele, Haplotype, Genotype

#                              rs7412 
#                              NC_000019.10:g.44908822
#                              C          T
#
# rs429358                 C   APOE-ε4    APOE-ε1
# NC_000019.10:g.44908684  T   APOE-ε3    APOE-ε2
# http://snpedia.com/index.php/APOE


sr = ObjectReference(namespace="NCBI", accession="NC_000019.10")

i429358 = Interval(44908683, 44908684)
i7412 = Interval(44908821, 44908822)

rs429358T = Allele(sr, i429358, "T")
rs429358C = Allele(sr, i429358, "C")
rs7412T = Allele(sr, i7412, "T")
rs7412C = Allele(sr, i7412, "C")

name_hap_map = {
    "ε1": Haplotype([rs429358C, rs7412T]),
    "ε2": Haplotype([rs429358T, rs7412T]),
    "ε3": Haplotype([rs429358T, rs7412C]),
    "ε4": Haplotype([rs429358C, rs7412C]),
    }
hap_name_map = {str(h.digest()): n for n, h in name_hap_map.items()}

haps = list(name_hap_map.values())

gts = [Genotype([haps[i], haps[j]])
       for i in range(len(haps))
       for j in range(i, len(haps))]

