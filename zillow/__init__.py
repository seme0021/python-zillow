#!/usr/bin/env python


"""
A library that provides a Python interface to the Zillow API
"""
from __future__ import absolute_import

__author__ = 'python-zillow@googlegroups.com'
__version__ = '0.1'


from .error import ZillowError
from .place import Place
from .api import ValuationApi