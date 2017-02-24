# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import attr
from attr.validators import instance_of, optional
import six

from vmc.digest import vmc_digest


@attr.s
@six.python_2_unicode_compatible
class ObjectReference(object):
    namespace = attr.ib(validator=instance_of(six.text_type))
    accession = attr.ib(validator=instance_of(six.text_type))

    def __str__(self):
        return "{self.namespace}:{self.accession}".format(self=self)

    def as_dict(self):
        return attr.asdict(self)

    def validate(self):
        attr.validate(self)


@attr.s
class Location(object):
    pass


@attr.s
@six.python_2_unicode_compatible
class Interval(Location):
    start = attr.ib(validator=instance_of(int))
    end = attr.ib(validator=instance_of(int))

    def __str__(self):
        return "<{self.start},{self.end}>".format(self=self)

    def as_dict(self):
        return attr.asdict(self)

    def validate(self):
        attr.validate(self)
        assert 0 <= self.start <= self.end

    def overlaps(self, other):
        assert isinstance(other, Interval)
        return self.end > other.start and other.end > self.start


@attr.s
class Allele(object):
    seqref = attr.ib(validator=instance_of(ObjectReference))
    location = attr.ib(validator=instance_of(Location))
    replacement = attr.ib(validator=instance_of(six.text_type))
    id = attr.ib(default=None, validator=optional(instance_of(ObjectReference)))

    #def __str__(self):
    #    return "{self.seqref}:{self.location}:{self.replacement}".format(self=self)

    def as_dict(self):
        return {
            "seqref": self.seqref.as_dict(),
            "location": self.location.as_dict(),
            "replacement": self.replacement,
            "id": str(self.digest)
            }

    @property
    def digest(self):
        binary_rep = "{self.seqref}:{self.location}:{self.replacement}".format(self=self).encode("UTF-8")
        return ObjectReference("GA", vmc_digest(binary_rep))

    def validate(self):
        attr.validate(self)


@attr.s
class Haplotype(object):
    alleles = attr.ib(validator=instance_of(list))
    id = attr.ib(default=None, validator=optional(instance_of(ObjectReference)))

    @property
    def allele_ids(self):
        return list(sorted(str(a.digest) for a in self.alleles))

    def as_dict(self):
        return {
            "allele_ids": list(map(str, self.allele_ids)),
            "id": str(self.digest)
            }

    @property
    def digest(self):
        binary_rep = ";".join(self.allele_ids).encode("UTF-8")
        return ObjectReference("GH", vmc_digest(binary_rep))

    def seqref(self):
        self.validate()
        return self.alleles[0].seqref

    def validate(self):
        attr.validate(self)
        for a in self.alleles:
            a.validate()
        if len(set(a.seqref for a in self.alleles)) != 1:
            raise ValueError("Haplotype alleles must be defined on the same sequence reference")
        for i in range(len(self.alleles) - 1):
            if self.alleles[i].location.start > self.alleles[i + 1].location.start:
                raise ValueError("Haplotype alleles must be ordered")
            if self.alleles[i].location.end > self.alleles[i + 1].location.start:
                raise ValueError("Haplotype alleles may not overlap")


@attr.s
class Genotype(object):
    haplotypes = attr.ib(validator=instance_of(list))
    id = attr.ib(default=None, validator=optional(instance_of(ObjectReference)))

    def as_dict(self):
        return {
            "haplotype_ids": list(map(str, self.haplotype_ids)),
            "id": str(self.digest)
            }

    @property
    def haplotype_ids(self):
        return list(sorted(str(h.digest) for h in self.haplotypes))

    @property
    def digest(self):
        binary_rep = ";".join(self.haplotype_ids).encode("UTF-8")
        return ObjectReference("GG", vmc_digest(binary_rep))

    def location(self):
        self.validate()
        return self.alleles[0].location

    def seqref(self):
        self.validate()
        return self.alleles[0].seqref

    def validate(self):
        attr.validate(self)
        for a in self.alleles:
            a.validate()
        if len(set(a.seqref for a in self.alleles)) != 1:
            raise ValueError("Genotype alleles must be defined on the same sequence reference")
        if len(set(a.location for a in self.alleles)) != 1:
            raise ValueError("Genotype alleles must be defined at the same Location")
        # TODO: Ensure Haplotypes are ordered (see haplotype ordering above)

