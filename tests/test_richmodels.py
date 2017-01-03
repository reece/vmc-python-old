from vmc.richmodels import Allele, Genotype, Haplotype, Interval, Location, ObjectReference


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

haplotypes = {
    "ε1": Haplotype([alleles["rs429358C"], alleles["rs7412T"]]),
    "ε2": Haplotype([alleles["rs429358T"], alleles["rs7412T"]]),
    "ε3": Haplotype([alleles["rs429358T"], alleles["rs7412C"]]),
    "ε4": Haplotype([alleles["rs429358C"], alleles["rs7412C"]]),

    # reverse order
    "ε2r": Haplotype([alleles["rs7412T"], alleles["rs429358T"]]),
    }

genotypes = {
    "ε2/ε2": Genotype([haplotypes["ε2"], haplotypes["ε2"]]),
    "ε2/ε3": Genotype([haplotypes["ε2"], haplotypes["ε3"]]),
    "ε3/ε2": Genotype([haplotypes["ε3"], haplotypes["ε2"]]),
    "ε3/ε3": Genotype([haplotypes["ε3"], haplotypes["ε3"]]),
    }


# Intervals
assert intervals["rs429358"] == intervals["rs429358"]
assert intervals["rs429358"].overlaps(intervals["rs429358"])
assert not intervals["rs429358"].overlaps(intervals["rs7412"])


# Alleles
assert alleles["rs429358T"] == alleles["rs429358T"]
assert alleles["rs429358T"] != alleles["rs429358C"]
assert alleles["rs429358T"] != alleles["rs7412C"]


# Haplotypes
assert haplotypes["ε2"] == haplotypes["ε2"]
assert haplotypes["ε3"] == haplotypes["ε3"]
assert haplotypes["ε2"] != haplotypes["ε3"]
# TODO: assert haplotypes["ε2"] == haplotypes["ε2r"], "haplotype equality should not depend on allele order"


# Genotypes
assert genotypes["ε2/ε2"] == genotypes["ε2/ε2"]
assert genotypes["ε3/ε3"] == genotypes["ε3/ε3"]
# TODO: assert genotypes["ε3/ε2"] == genotypes["ε2/ε3"], "genotype equality should not depend on haplotype order"
