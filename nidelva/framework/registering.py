#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Use absolute path since this module is initialized first
from nidelva.platform import logging

__all__ = ['RegistryOverrideException', 'Registry']

class RegistryOverrideException (Exception):
    """Thrown when a name is overridden implicitly."""
    pass

class Registry (object):
    """A key-value store for objects."""

    def __init__ (self):
        """Makes a new registry."""
        self._mapping = dict()

    def __contains__ (self, key):
        return key in self._mapping

    def register (self, key, value, override=False):
        """Registers key -> value mapping."""
        if not override and key in self._mapping:
            raise RegistryOverrideException (
                'Registering key "{key}" for value "{value}" when '
                'key is already registered for "{old_value}"'.format (
                    key=key, value=value, old_value=self._mapping[key]
                )
            )

        logging.debug (
            'registered {key} -> {value} in {self}'.format (
                key=key, value=value, self=self
            )
        )

        self._mapping[key] = value
        return value

    def retrieve (self, key):
        """Returns value based on key."""
        return self._mapping[key]

    def as_list (self):
        """Returns the registered keys as a list."""
        return list(self._mapping.keys())
