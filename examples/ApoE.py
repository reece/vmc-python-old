from vmc.models import SequenceReference, Interval, Allele, Haplotype, Genotype

#                              rs7412 
#                              NC_000019.10:g.44908822
#                              C          T
#
# rs429358                 C   APOE-ε4    APOE-ε1
# NC_000019.10:g.44908684  T   APOE-ε3    APOE-ε2
# http://snpedia.com/index.php/APOE


sr = SequenceReference(namespace="NCBI", accession="NC_000019.10")

i429358 = Interval(44908683, 44908684)
i7412 = Interval(44908821, 44908822)

rs429358T = Allele(sr, i429358, "T")
rs429358C = Allele(sr, i429358, "C")
rs7412T = Allele(sr, i7412, "T")
rs7412C = Allele(sr, i7412, "C")

apoe1 = Haplotype([rs429358C, rs7412T])
apoe2 = Haplotype([rs429358T, rs7412T])
apoe3 = Haplotype([rs429358T, rs7412C])
apoe4 = Haplotype([rs429358C, rs7412C])

