#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import configs
import utility

import numpy as np

register = {}

class Environment (object):
    """Base class for environments."""
    def __init__ (self, state_config, action_config):
        self.state_config = state_config
        self.action_config = action_config

    def reset (self):
        raise NotImplementedError()

    def step (self, action):
        raise NotImplementedError()

@utility.registered(register, 'Customer')
class CustomerEnvironment (Environment):
    """Models a customer."""
    def __init__ (
            self,
            n_up_actions, n_down_actions,
            starting_usage, starting_quota,
            quota_increment,
            usage_increment_fn
    ):
        # Total number of actions
        n_actions = 1 + n_up_actions + n_down_actions

        # Set up data configs
        state_config = configs.DataConfig(dtype='float', shape=[2])
        action_config = configs.DataConfig(dtype='int', shape=[n_actions])

        super(CustomerEnvironment, self).__init__ (
            state_config=state_config,
            action_config=action_config
        )

        # General parameters
        self.n_up_actions = n_up_actions
        self.n_down_actions = n_down_actions
        self.usage_increment_fn = usage_increment_fn

        # Reset parameters
        self.starting_usage = starting_usage
        self.starting_quota = starting_quota
        self.quota_increment = quota_increment

        # TODO: Numpy random state?

        # Step values
        self.quota = None
        self.usage = None
        self.step_counter = None

    def state (self):
        """Returns the current state/observation.""" 
        return np.stack([self.usage, self.quota])

    def reset (self):
        """Resets the environment."""
        self.step_counter = 0

        self.quota = self.starting_quota
        self.usage = self.starting_usage

        # TODO: Numpy random state?

        return self.state()

    def get_level_by_action (self, action):
        """Returns the level of the given action."""
        n_positive_actions = 1 + self.n_up_actions

        # NO-OP and upsells
        if action < n_positive_actions:
            return action

        # Downsells
        return n_positive_actions - (1+action)

    def get_level_by_quota (self, target_quota):
        """Returns the level needed to adjust quota to target."""
        delta_quota = target_quota - self.quota

        # Use absolute value to avoid float round-off of negative values
        levels = np.abs(delta_quota)//self.quota_increment

        return levels if delta_quota >= 0.0 else -levels

    def step (self, action):
        """Takes an action in the current environment."""
        action_level = self.get_level_by_action(action)

        # Update internal values
        self.step_counter += 1
        self.usage += self.usage_increment_fn()
        self.quota += action_level*self.quota_increment

        # Calculate outputs
        reward = self.quota/self.quota_increment
        terminal = False
        info = {
            'step_counter' : self.step_counter,
            'usage' : self.usage,
            'quota' : self.quota,
            'action_level' : action_level
        }

        return self.state(), reward, terminal, info
