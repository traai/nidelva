#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import configs
import environments

# TODO: Belongs in a separate file/directory
def make_linear_usage_fn (a, b):
    def usage_fn (step):
        return a*step + b

    return usage_fn

class Simulator (object):
    env_fns = {
        'Customer' : environments.CustomerEnvironment
    }

    # TODO: Belongs in a separate file/directory
    usage_fns = {
        'linear' : make_linear_usage_fn
    }

    def __init__ (self):
        self.config = None

    def load_config (self, config):
        self.config = config
        return self

    def build_environment (self):
        # Create temporary copy since we're mutating it
        config = dict(self.config)

        # Get environment type
        env_fn = self.env_fns[config.pop('environment')]

        # Set up data configs
        state_config = configs.DataConfig.from_dict(config.pop('state_config'))
        action_config = configs.DataConfig.from_dict(config.pop('action_config'))

        # Create usage_fn
        usage_fn_config = config.pop('usage_fn')
        make_usage_fn = self.usage_fns[usage_fn_config.pop('type')]
        usage_fn = make_usage_fn(**usage_fn_config)

        # Return environment
        return env_fn (
            state_config=state_config,
            action_config=action_config,
            usage_fn=usage_fn,
            # Pass remaining configurations as-is
            **config
        )
