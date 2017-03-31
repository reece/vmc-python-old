from __future__ import unicode_literals

from bioutils.truncated_digest import truncated_digest



def vmc_digest(binary_data):
    return truncated_digest(binary_data, digest_size=24)



# def _allele_digest(o):
#     u = "{o.seqref}:{o.location}:{o.replacement}".format(o=o)
#     b = u.encode("UTF-8")
#     return truncated_digest(b)
# 
# def _haplotype_digest(o):
#     u = "{o.seqref}:{o.location}:{o.replacement}".format(o=o)
#     b = u.encode("UTF-8")
#     return truncated_digest(b)
# 
# 
# def vmc_digest(o):
#     """returns digest for object o"""

        
