#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import configs
import functions
import environments

class Simulator (object):
    def __init__ (self):
        self.config = None

    def load_config (self, config):
        self.config = config
        return self

    def build_environment (self):
        # Create temporary copy since we're mutating it
        config = dict(self.config)

        # Get environment type
        env_fn = environments.register[config.pop('environment')]

        # Set up data configs
        if 'state_config' in config:
            config['state_config'] = configs.DataConfig.from_dict(config['state_config'])
        if 'action_config' in config:
            config['action_config'] = configs.DataConfig.from_dict(config['action_config'])

        # For _fn endings create the function and modify config in-place
        for key in config:
            if not key.endswith('_fn'):
                continue

            fn_config = config[key]
            make_fn = functions.register[fn_config.pop('type')]
            config[key] = make_fn(**fn_config)

        # Return environment
        return env_fn (
            **config
        )
