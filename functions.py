#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import utility
import numpy as np

register = {}

@utility.registered(register, 'constant')
def make_constant_fn (value):
    """Creates a constant value function."""

    def constant_fn ():
        """Function that returns a constant."""
        return value

    return constant_fn

@utility.registered(register, 'normal')
def make_normal_fn (mean, standard_deviation):
    """Creates a function returning samples from a normal distribution."""

    def normal_fn ():
        """Returns a sample from normal distribution."""
        return np.random.normal(loc=mean, scale=standard_deviation)

    return normal_fn
