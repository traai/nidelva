#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['export', 'fetch']

# Before we do anything else create global registry and decorator
from nidelva.framework import registering
from nidelva.framework import exporting
from nidelva.framework import fetching

global_registry = registering.Registry()
export = exporting.Exporter(registry=global_registry)
fetch = fetching.Fetcher(registry=global_registry).fetch
