#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['Exporter']

class AutoExportDecorator (object):
    """Function decorator that registers objects into a registry by automatically generating a handle."""

    def __init__ (self, registry):
        """Makes a new decorator with the given registry."""
        self._registry = registry

    def __call__ (self, obj):
        """Creates a handle and registers the object then returns the object unmodified."""
        handle = '.'.join([obj.__module__, obj.__name__])
        self._registry.register(handle, obj)
        return obj

class ExportDecorator (object):
    """Function decorator that registers objects into a registry with a given handle."""

    def __init__ (self, registry, handle):
        """Makes a new decorator with the given registry and handle."""
        self._registry = registry
        self._handle = handle

    def __call__ (self, obj):
        """Registers obj in registry by handle then returns the object unmodified."""
        self._registry.register(self._handle, obj)
        return obj

class Exporter (object):
    """A factory for function decorators that register symbols into a Registry."""

    @staticmethod
    def args_to_handle (args):
        return '.'.join(args)

    def __init__ (self, registry):
        """Makes a new exporter based on a registry."""
        self._registry = registry

    def __call__ (self, *args):
        """Creates function decorator for the given handle."""
        return ExportDecorator(registry=self._registry, handle=self.args_to_handle(args))

    @property
    def auto (self):
        """Creates function decorator that automatically creates a handle."""
        return AutoExportDecorator(registry=self._registry)

    def existing (self, obj, *args):
        """Registers an existing object with a handle."""
        return self._registry.register(self.args_to_handle(args), obj)
