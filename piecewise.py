#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import nidelva

import numpy as np

configs = {
    'noop'     : 'env_configs/stable_noop.json',
    'upsale'   : 'env_configs/stable_upsale.json',
    'downsale' : 'env_configs/stable_downsale.json',
}

class PiecewiseIncrement (object):
    def __init__ (self, initial_value, num_steps, increments):
        self.last_step = 0
        self.num_steps = num_steps
        self.current_value = initial_value

        self.increments = increments

    def should_change_scenario (self, env):
        if self.current_value is None:
            return True

        # TODO: Some other logic here??
        return env.step_counter.value >= self.last_step + self.num_steps

    def select_increment (self, env):
        # Choose new increment
        increments = self.increments[:]

        # If usage is 0, filter out any negative increments as we can't
        # really do a useful downsale scenario here.
        if env.usage.value == 0:
            increments = [x for x in increments if x > 0]

        # Pick one at random
        # TODO: Some logic here??
        return np.random.choice(increments)

    def __call__ (self, env):
        if self.should_change_scenario(env):
            # Update new usage increment
            self.current_value = self.select_increment(env)

            # Update step mark
            self.last_step = env.step_counter.value

        # Give increment
        return self.current_value

def main (FLAGS):
    if FLAGS.debug:
        nidelva.logging.set_verbosity(nidelva.logging.DEBUG)

    # Load parameters from every scenario
    for name in configs:
        with open(configs[name], 'r') as in_file:
            configs[name] = json.load(in_file)

    increments = [
        configs['noop']['usage_increment'],
        configs['upsale']['usage_increment'],
        configs['downsale']['usage_increment'],
    ]

    # Master copy
    config = configs['noop']
    config['usage_increment'] = PiecewiseIncrement (
        initial_value=None, num_steps=FLAGS.scenario_steps, increments=increments
    )

    # Fetch and initialize env from library
    env = nidelva.fetch(config)

    state = env.reset()
    step, action, terminal = 0, 0, False
    while not terminal and step < FLAGS.max_steps:
        state, reward, terminal, info = env.step(action)
        step += 1

        print(info)
        action = info['expected_action']

    return 0

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument (
        '--debug', action='store_true',
        help='Turn on debugging information.'
    )

    parser.add_argument (
        '--max_steps', type=int, default=1000, metavar='n',
        help='Max number of steps to run environment for.'
    )

    parser.add_argument (
        '--scenario_steps', type=int, default=250, metavar='n',
        help='Max number of steps to run each scenario for.'
    )

    FLAGS = parser.parse_args()
    exit(main(FLAGS))
