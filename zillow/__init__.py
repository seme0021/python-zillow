"""A library that provides a Python interface to the Zillow API."""

from __future__ import absolute_import

import os as _os
import pkg_resources as _pkg_resources

from .error import ZillowError  # noqa: F401
from .place import Place  # noqa: F401
from .api import ValuationApi  # noqa: F401


__author__ = 'python-zillow@googlegroups.com'


try:
    _dist = _pkg_resources.get_distribution('python-' + __package__)
    if not _os.path.abspath(__file__).startswith(
            _os.path.join(_dist.location, __package__)):
        # Manually raise the exception if there is a distribution but
        # it's installed from elsewhere.
        raise _pkg_resources.DistributionNotFound
except _pkg_resources.DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version
