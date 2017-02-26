# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import attr
from attr.validators import instance_of, optional
import six

from vmc.digest import vmc_digest


@attr.s
class Location(object):
    pass


@attr.s
@six.python_2_unicode_compatible
class Interval(Location):
    start = attr.ib(validator=instance_of(int))
    end = attr.ib(validator=instance_of(int))

    def __bytes__(self):
        return self.__str__().encode("UTF-8")

    def __str__(self):
        return "{self.start}:{self.end}".format(self=self)

    def as_dict(self):
        return attr.asdict(self)

    def validate(self):
        attr.validate(self)
        assert 0 <= self.start <= self.end

    def overlaps(self, other):
        assert isinstance(other, Interval)
        return self.end > other.start and other.end > self.start


@attr.s
class Locus(object):
    seqref = attr.ib(validator=instance_of(str))
    location = attr.ib(validator=instance_of(Location))
    id = attr.ib(default=None, validator=optional(instance_of(str)),  cmp=False)

    @property
    def identifier(self):
        if self.id is None:
            self.id = self.computed_identifer()
        return self.id

    def __bytes__(self):
        return self.__str__().encode("UTF-8")

    def __str__(self):
        return "{self.seqref}:{self.location}".format(self=self)

    def as_dict(self):
        return attr.asdict(self)

    def computed_identifer(self):
        return "GL:" + self.digest()

    def digest(self):
        return vmc_digest(bytes(self))

    def validate(self):
        attr.validate(self)
        self.seqref.validate()
        self.location.validate()


@attr.s
class Allele(object):
    seqref = attr.ib(validator=instance_of(str))
    location = attr.ib(validator=instance_of(Location))
    replacement = attr.ib(validator=instance_of(six.text_type))
    id = attr.ib(default=None, validator=optional(instance_of(str)), cmp=False)

    @property
    def identifier(self):
        if self.id is None:
            self.id = self.computed_identifer()
        return self.id

    def __bytes__(self):
        return self.__str__().encode("UTF-8")

    def __str__(self):
        return "{self.seqref}:{self.location}:{self.replacement}".format(self=self)

    def as_dict(self):
        return attr.asdict(self)

    def computed_identifer(self):
        return "GA:" + self.digest()

    def digest(self):
        return vmc_digest(bytes(self))

    def validate(self):
        attr.validate(self)
        self.locus.validate()
        self.validate()


@attr.s
class Haplotype(object):
    alleles = attr.ib(validator=instance_of(list))
    id = attr.ib(default=None, validator=optional(instance_of(str)), cmp=False)

    @property
    def identifier(self):
        if self.id is None:
            self.id = self.computed_identifer()
        return self.id

    def allele_ids(self):
        # return unicode allele identifiers in UTF-8 encoded order
        # encoding eliminates effects of locale-specific collation order 
        ids = [o.identifier for o in self.alleles]
        ids.sort(key=lambda e: e.encode("UTF-8"))
        return ids

    def as_dict(self):
        return {
            "allele_ids": self.allele_ids(),
            "id": self.identifier
        }

    def computed_identifer(self):
        return "GH:" + self.digest()

    def digest(self):
        return vmc_digest(";".join(self.allele_ids()).encode("UTF-8"))

    def validate(self):
        attr.validate(self)
        if len(set(a.locus.seqref for a in self.alleles)) != 1:
            raise ValueError("Haplotype alleles must be defined on exactly one sequence")
        # TODO: validate that alleles do not overlap



@attr.s
class Genotype(object):
    haplotypes = attr.ib(validator=instance_of(list))
    id = attr.ib(default=None, validator=optional(instance_of(str)), cmp=False)

    @property
    def identifier(self):
        if self.id is None:
            self.id = self.computed_identifier()
        return self.id

    def as_dict(self):
        return {
            "haplotype_ids": self.haplotype_ids(),
            "id": self.identifier
        }

    def computed_identifier(self):
        return "GG:" + self.digest()

    def digest(self):
        return vmc_digest(";".join(self.haplotype_ids()).encode("UTF-8"))

    def haplotype_ids(self):
        # return unicode haplotype identifiers in UTF-8 encoded order
        # encoding eliminates effects of locale-specific collation order 
        ids = [o.identifier for o in self.haplotypes]
        ids.sort(key=lambda e: e.encode("UTF-8"))
        return ids

    def validate(self):
        attr.validate(self)


if __name__ == "__main__":
    import json

    import vmc.codecs.json

    def to_json(o):
        return json.dumps(o, indent=2, sort_keys=True, cls=vmc.codecs.json.JSONEncoder, ensure_ascii=False)


    sr = "NCBI:NC_000019.10"
    intervals = {
        "rs429358": Interval(44908683, 44908684),
        "rs7412": Interval(44908821, 44908822),
    }
    o = intervals["rs429358"]
    print("r={o!r}\ns={o}\nj={j}".format(o=o, j=to_json(o)))


    loci = {
        "rs429358": Locus(sr, intervals["rs429358"]),
        "rs7412": Locus(sr, intervals["rs7412"]),
    }
    o = loci["rs429358"]
    print("r={o!r}\ns={o}\nid={o.identifier}\nj={j}".format(o=o, j=to_json(o)))


    alleles = {
        "rs429358T": Allele(sr, intervals["rs429358"], "T"),
        "rs429358C": Allele(sr, intervals["rs429358"], "C"),
        "rs7412T":   Allele(sr, intervals["rs7412"],   "T"),
        "rs7412C":   Allele(sr, intervals["rs7412"],   "C"),
    }
    o = alleles["rs429358C"]
    print("r={o!r}\ns={o}\nid={o.identifier}\nj={j}".format(o=o, j=to_json(o)))

    haplotypes = {
        "ε1": Haplotype([alleles["rs429358C"], alleles["rs7412T"]]),
        "ε2": Haplotype([alleles["rs429358T"], alleles["rs7412T"]]),
        "ε3": Haplotype([alleles["rs429358T"], alleles["rs7412C"]]),
        "ε4": Haplotype([alleles["rs429358C"], alleles["rs7412C"]]),
        "ε4r": Haplotype([alleles["rs7412C"], alleles["rs429358C"]]),
    }
    o = haplotypes["ε1"]
    print("r={o!r}\ns={o}\nid={o.identifier}\nj={j}".format(o=o, j=to_json(o)))

    genotypes = {
        "{}/{}".format(h1n, h2n): Genotype([h1, h2])
        for h1n, h1 in haplotypes.items()
        for h2n, h2 in haplotypes.items()
        }
    o = genotypes["ε1/ε1"]
    print("r={o!r}\ns={o}\nid={o.identifier}\nj={j}".format(o=o, j=to_json(o)))
