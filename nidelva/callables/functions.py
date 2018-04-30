#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from nidelva import export

@export('function', 'constant')
def make_constant_fn (value):
    """Creates a constant value function."""

    # FIXME: This *args, **kwargs stuff needs to be handled in _make_callable
    # of nidelva.callables.classes somehow.
    def constant_fn (*args, **kwargs):
        """Function that returns a constant."""
        return value

    return constant_fn

@export('function', 'normal')
def make_normal_fn (mean, standard_deviation, random_state=np.random):
    """Creates a function returning samples from a normal distribution."""

    def normal_fn (*args, **kwargs):
        """Returns a sample from normal distribution."""
        return random_state.normal(loc=mean, scale=standard_deviation)

    return normal_fn
