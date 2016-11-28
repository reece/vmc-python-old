# -*- coding: utf-8 -*-
# pragma: nocover

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import pkg_resources
import warnings

logger = logging.getLogger(__name__)

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound as e:  # pragma: no cover
    warnings.warn("can't get __version__ because %s package isn't installed" % __package__, Warning)
    __version__ = None

logger.info(__name__ + " " + __version__)
