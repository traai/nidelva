#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json

__all__ = ['Fetcher']

class Fetcher (object):
    """A class that resolves handles and configs into objects."""

    def __init__ (self, registry):
        """Makes a new fetcher backed by a registry."""
        self._registry = registry

    def fetch (self, handle):
        """Fetches value based on handle."""
        if isinstance(handle, str):
            return self._registry.retrieve(handle)
        if isinstance(handle, collections.Mapping):
            if 'type' in handle:
                params = dict(handle)
                obj = self._registry.retrieve(params.pop('type'))

                # Cascade onto children
                for key in params:
                    params[key] = self.fetch(params[key])

                return obj(**params)

        return handle

    def from_json (self, in_file):
        """Fetches contents from json file."""
        return self.fetch(json.load(in_file))
