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
            usage_increment_fn,
            annoyance_per_miss, annoyance_threshold,
            overusage_threshold, churn_threshold
    ):
        # Total number of actions
        n_actions = 1 + n_up_actions + n_down_actions

        # Set up data configs
        state_config = configs.DataConfig(dtype='float', shape=[3])
        action_config = configs.DataConfig(dtype='int', shape=[n_actions])

        super(CustomerEnvironment, self).__init__ (
            state_config=state_config,
            action_config=action_config
        )

        # General parameters
        self.n_up_actions = n_up_actions
        self.n_down_actions = n_down_actions

        self.usage_increment_fn = usage_increment_fn
        self.quota_increment = quota_increment
        self.annoyance_per_miss = annoyance_per_miss
        self.annoyance_threshold = annoyance_threshold
        self.overusage_threshold = overusage_threshold
        self.churn_threshold = churn_threshold

        # Reset parameters
        self.starting_usage = starting_usage
        self.starting_quota = starting_quota

        # TODO: Numpy random state?

        # Step values
        self.quota = None
        self.usage = None
        self.step_counter = None
        self.annoyance = None
        self.expected_action = None
        self.expected_counter = None
        self.churn_flag = None
        self.churn_counter = None

    def state (self):
        """Returns the current state/observation.""" 
        return np.stack([self.usage, self.quota, self.churn_flag])

    def reset (self):
        """Resets the environment."""
        self.step_counter = 0

        self.quota = self.starting_quota
        self.usage = self.starting_usage
        self.annoyance = 0.0
        self.expected_action = 0
        self.overusage_counter = 0
        self.churn_flag = 0
        self.churn_counter = 0

        # TODO: Numpy random state?

        return self.state()

    def get_level_by_action (self, action):
        """Returns the level of the given action."""
        n_positive_actions = 1 + self.n_up_actions

        # NO-OP and upsell actions
        if action < n_positive_actions:
            return action

        # Downsell actions
        return n_positive_actions - (1+action)

    def get_action_by_level (self, level):
        """Inverse mapping of get_level_by_action."""
        n_positive_actions = 1 + self.n_up_actions

        # NO-OP and upsell actions
        if level >= 0:
            # Snap to action space
            return level if level < n_positive_actions else n_positive_actions-1

        # Downsell actions
        level = -(1+level)

        # Snap to action space
        return level if level < self.n_down_actions else self.n_down_actions-1

    def get_level_by_quota (self, target_quota):
        """Returns the level needed to adjust quota to target."""
        delta_quota = target_quota - self.quota

        # Use absolute value to avoid float round-off of negative values
        levels = np.abs(delta_quota)//self.quota_increment

        return int(levels if delta_quota >= 0.0 else -levels)

    def step (self, action):
        """Takes an action in the current environment."""
        action_level = self.get_level_by_action(action)

        # Update internal values
        self.step_counter += 1
        self.usage += self.usage_increment_fn()
        self.quota += action_level*self.quota_increment

        # Deal with overusage
        if self.usage > self.quota:
            self.overusage_counter += 1
        else:
            self.overusage_counter = 0

        # If overusage exceeds threshold we expect upsell
        if self.overusage_counter >= self.overusage_threshold:
            expected_level = self.get_level_by_quota(target_quota=self.usage)
            self.expected_action = self.get_action_by_level(expected_level)

        # Get annoyed if agent doesn't give expected action
        if action != self.expected_action:
            self.annoyance += self.annoyance_per_miss
        else:
            self.annoyance -= self.annoyance_per_miss

            # Snap to [0, ...]
            if self.annoyance < 0.0:
                self.annoyance = 0.0

        # Send complaint if annoyance exceeds threshold
        self.churn_flag = np.float32(self.annoyance >= self.annoyance_threshold)

        # If complaint goes unanswered for too long, quit
        if self.churn_flag > 0.0:
            self.churn_counter += 1
        else:
            self.churn_counter = 0

        terminal = self.churn_counter >= self.churn_threshold

        # Calculate outputs
        reward = self.quota/self.quota_increment
        info = {
            'step_counter' : self.step_counter,
            'usage' : self.usage,
            'quota' : self.quota,
            'churn_flag' : self.churn_flag,
            'churn_counter' : self.churn_counter,
            'annoyance' : self.annoyance,
            'expected_action' : self.expected_action,
            'overusage_counter' : self.overusage_counter,
            'action_level' : action_level
        }

        return self.state(), reward, terminal, info
