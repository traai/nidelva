#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import utility

register = {}

@utility.registered(register, 'linear')
def make_linear_fn (slope, offset):
    """Creates a linear function y = slope*x + offset."""

    def usage_fn (x):
        """Linear function y = slope*x + offset."""
        return slope*x + offset

    return usage_fn
