import itertools
import json
import re

import hgvs.parser

from vmc.richmodels import Allele, Interval


uri_re = re.compile("([^:]+):(.+)")   
hp = hgvs.parser.Parser()


def multimap(iter, invert=False):
    """for an interable with (k,v) tuples like [(k1,v1a), (k1,v1b),
    (k2,v2), ...], return a dictionary mapping {k: [v]}

    >>> names_ages = [("Alice", 3), ("Bob", 7), ("Charlie", 7)]

    >>> multimap((a,n) for n,a in names_ages)
    {3: ['Alice'], 7: ['Bob', 'Charlie']}

    >>> multimap(kids, invert=True)
    {3: ['Alice'], 7: ['Bob', 'Charlie']}

    """

    iter2 = ((b, a) for a, b in iter) if invert else iter
    i = itertools.groupby(sorted(iter2), lambda e: e[0])
    return {k: list(e[1] for e in ei) for k, ei in i}



def seq_id(sr, uri):
    namespace, alias = uri_re.match(uri).groups()
    namespace = namespace.lower()
    aliases = sr.aliases.find_aliases(namespace="ncbi", alias="NC_000019.10").fetchall()
    return "GS:" + aliases[0]["seq_id"]


def hgvs_to_Allele(hgvs):
    var = hp.parse_hgvs_variant(hgvs)
    return Allele(seqref=var.ac,
                  location=Interval(var.posedit.pos.start-1, var.posedit.pos.end),
                  replacement=var.posedit.edit.alt)
