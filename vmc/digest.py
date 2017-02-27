from __future__ import unicode_literals

from bioutils.truncated_digest import truncated_digest

def vmc_digest(binary_data):
    return truncated_digest(binary_data, digest_size=24)
