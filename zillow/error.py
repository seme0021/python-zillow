#!/usr/bin/env python

class ZillowError(Exception):
    """Base class for Twitter errors"""

    @property
    def message(self):
        """
        :return: The first argument used to construct this error.
        """
        return self.args[0]