#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from nidelva import export

from nidelva.callables.classes import Counter, Trigger
from nidelva.configs import DataConfig
from nidelva.environments import Environment, extern_gym
from nidelva.platform import logging

import numpy as np

__all__ = ['CustomerEnvironment']

@export('environment', 'Customer')
class CustomerEnvironment (Environment):
    """Models a customer."""

    def __init__ (
            self,
            n_up_actions, n_down_actions,
            starting_usage, starting_quota,
            quota_increment, usage_increment,
            annoyance_per_miss,
            annoyance_threshold,
            terminal_annoyance,
            overusage_threshold,
            reward
    ):
        # Total number of actions
        n_actions = 1 + n_up_actions + n_down_actions

        # Set up data configs
        state_config = DataConfig(dtype='float', shape=[3])
        action_config = DataConfig(dtype='int', shape=[n_actions])

        super(CustomerEnvironment, self).__init__ (
            state_config=state_config,
            action_config=action_config
        )

        # Set up OpenAI gym compatibility layer
        if extern_gym is not None:
            self.observation_space = extern_gym.spaces.Box (
                low=np.array([0.0, 0.0, 0.0]),
                high=np.array([1000.0, 1000.0, 1.0]),
                dtype=state_config.dtype_numpy
            )

            self.action_space = extern_gym.spaces.Discrete(n_actions)

        # General parameters
        self.n_up_actions = n_up_actions
        self.n_down_actions = n_down_actions

        self.quota_increment = quota_increment

        # TODO: Numpy random state?

        self.quota = Counter (
            initial_value = starting_quota,
            increment = lambda self : self.action_level * self.quota_increment,
            condition = lambda self : self.expected_action.value == self.action,
            lower_limit=0.0
        )

        self.usage = Counter (
            initial_value=starting_usage, increment=usage_increment,
            lower_limit=0.0
        )

        self.step_counter = Counter (
            initial_value=0, increment=1
        )

        self.expected_action = Trigger (
            initial_value=0,
            trigger_value = lambda self : self.get_expected_action(self.usage.value),
            reset_on_false=True
        )

        def annoyance_increment (self):            
            if self.action == self.expected_action.value:
                return -annoyance_per_miss
            return annoyance_per_miss

        self.annoyance = Counter (
            initial_value=0.0, lower_limit=0.0,
            increment = annoyance_increment 
        )

        self.churn = Trigger (
            initial_value=0.0, trigger_value=1.0,
            condition = lambda self : self.annoyance.value >= annoyance_threshold,
            reset_on_false=True
        )

        self.terminal = Trigger (
            initial_value=False, trigger_value=True,
            condition = lambda self : self.annoyance.value >= terminal_annoyance
        )

        self.reward = Trigger (
            initial_value=0.0, trigger_value=reward
        )

    def state (self):
        """Returns the current state/observation.""" 
        return np.stack([self.usage.value, self.quota.value, self.churn.value])

    def reset (self):
        """Resets the environment."""
        self.step_counter.reset()
        self.quota.reset()
        self.usage.reset()
        self.annoyance.reset()
        self.churn.reset()
        self.expected_action.reset()
        self.terminal.reset()
        self.reward.reset()

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
        if level >= self.n_down_actions-1:
            level = self.n_down_actions-1

        # Snap to action space
        return n_positive_actions + level

    def get_level_by_quota (self, target_quota):
        """Returns the level needed to adjust quota to target."""
        delta_quota = target_quota - self.quota.value

        # Use absolute value to avoid float round-off of negative values
        levels = np.abs(delta_quota)//self.quota_increment

        return int(levels if delta_quota >= 0.0 else -levels)

    def get_expected_action (self, target_quota):
        """Returns the expected action based on a target quota."""
        expected_level = self.get_level_by_quota(target_quota)
        return self.get_action_by_level(expected_level)

    def step (self, action):
        """Takes an action in the current environment."""
        self.action = action
        self.action_level = self.get_level_by_action(action)
        self.expected_action.step(self)

        # Update internal values
        self.step_counter.step()
        self.usage.step(self)
        self.quota.step(self)

        # Get annoyed if agent doesn't give expected action
        self.annoyance.step(self)

        # Send complaint if annoyance exceeds threshold
        self.churn.step(self)

        # If complaint goes unanswered for too long, quit
        terminal = self.terminal.step(self)

        # Calculate outputs
        reward = self.reward.step(self)
        info = {
            'step_counter' : self.step_counter.value,
            'usage' : self.usage.value,
            'quota' : self.quota.value,
            'churn' : self.churn.value,
            'annoyance' : self.annoyance.value,
            'expected_action' : self.expected_action.value,
            'action_level' : self.action_level
        }

        return self.state(), reward, terminal, info
