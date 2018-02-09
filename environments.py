#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import utility
import numpy as np

environment_fns = {}

class Environment (object):
    """Base class for environments."""
    def __init__ (self, state_config, action_config):
        self.state_config = state_config
        self.action_config = action_config

    def reset (self):
        raise NotImplementedError()

    def step (self, action):
        raise NotImplementedError()

@utility.registered(environment_fns, 'Customer')
class CustomerEnvironment (Environment):
    """Models a customer."""
    def __init__ (self, state_config, action_config, usage_fn, starting_quota):
        super(CustomerEnvironment, self).__init__ (
            state_config=state_config,
            action_config=action_config
        )

        self.usage_fn = usage_fn
        self.starting_quota = starting_quota

        self.quota = None
        self.usage = None
        self.counter = None

    def state (self):
        self.usage = self.usage_fn(self.counter)
        # TODO: Want checking/conversion of dtype and shape to conform to DataConfig?
        return np.stack([self.usage, self.quota])

    def reset (self):
        self.counter = 0
        self.quota = self.starting_quota

        return self.state()

    def step (self, action):
        self.counter += 1

        # TODO: Modify all internal state based on action
        # self.quota = quota_fn(self.quota, action)?
        # self.annoyance_level = ...

        reward = 0
        terminal = False

        # TODO: Full hidden state, like counter, random seed etc.
        # can be included here for plotting on user side
        info = {}

        return self.state(), reward, terminal, info
