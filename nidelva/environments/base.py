#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# FIXME: This gym import needs to be abstracted?
# FIXME: Should be in some global configuration dict?
try:
    import gym as extern_gym
except ImportError:
    logging.debug('Failed to import gym')
    extern_gym = None

__all__ = ['Environment', 'extern_gym']

class Environment (object):
    """Base class for environments."""

    def __init__ (self, state_config, action_config):
        """Makes a new environment."""
        self.state_config = state_config
        self.action_config = action_config

    def reset (self):
        """Resets the environment to initial state and returns this state."""
        raise NotImplementedError()

    def step (self, action):
        """Takes action in environment, return state, reward, terminal and info dict."""
        raise NotImplementedError()
