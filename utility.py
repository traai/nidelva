#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def registered (mapping, handle):
    """Creates a decorator that registers an object in a mapping with a handle."""

    def decorator_fn (obj):
        """Registers an object in a mapping then passes it without modification."""
        mapping[handle] = obj
        return obj

    return decorator_fn
