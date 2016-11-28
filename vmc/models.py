# -*- coding: utf-8 -*-

import base64
import hashlib
import re

import attr
from attr.validators import instance_of
import six


@attr.s
@six.python_2_unicode_compatible
class SequenceReference(object):
    namespace = attr.ib(validator=instance_of(str))
    accession = attr.ib(validator=instance_of(str))

    def validate(self):
        attr.validate(self)

    def __str__(self):
        return "{self.namespace}/{self.accession}".format(self=self)


@attr.s
@six.python_2_unicode_compatible
class Interval(object):
    start = attr.ib(validator=instance_of(int))
    end = attr.ib(validator=instance_of(int))

    def validate(self):
        attr.validate(self)
        assert self.start <= self.end

    def overlaps_with(self, other):
        assert isinstance(other, Interval)
        return self.end > other.start and other.end > self.start

    def __str__(self):
        return "<{self.start},{self.end}>".format(self=self)


@attr.s
@six.python_2_unicode_compatible
class Allele(object):
    seqref = attr.ib(validator=instance_of(SequenceReference))
    interval = attr.ib(validator=instance_of(Interval))
    replacement = attr.ib(validator=instance_of(str))

    def validate(self):
        attr.validate(self)

    def __str__(self):
        return "{self.seqref}:{self.interval}:{self.replacement}".format(self=self)


@attr.s
@six.python_2_unicode_compatible
class Haplotype(object):
    alleles = attr.ib(validator=instance_of(list))

    def validate(self):
        attr.validate(self)
        if len(set(a.seqref for a in self.alleles)) != 1:
            raise ValueError("Haplotype alleles must be defined on the same sequence reference")
        for i in range(len(self.alleles) - 1):
            if self.alleles[i].interval.start > self.alleles[i + 1].interval.start:
                raise ValueError("Haplotype alleles must be ordered")
            if self.alleles[i].interval.end > self.alleles[i + 1].interval.start:
                raise ValueError("Haplotype alleles may not overlap")


@attr.s
@six.python_2_unicode_compatible
class Genotype(object):
    haplotypes = attr.ib(validator=instance_of(list))

    def validate(self):
        attr.validate(self)
        if len(set(a.seqref for a in self.alleles)) != 1:
            raise ValueError("Genotype alleles must be defined on the same sequence reference")
        if len(set(a.interval for a in self.alleles)) != 1:
            raise ValueError("Genotype alleles must be defined at the same interval")
