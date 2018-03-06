#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import nidelva

# Modify reward function at runtime
@nidelva.export('reward_fn')
def correct_action_reward (self):
    # Reward correct action
    return float(self.action == self.expected_action.value)

def main (FLAGS):
    if FLAGS.debug:
        nidelva.logging.set_verbosity(nidelva.logging.DEBUG)

    with open(FLAGS.config, 'r') as in_file:
        config = json.load(in_file)

    # Modify reward function at runtime
    config['reward'] = 'reward_fn'

    # Fetch and initialize env from library
    env = nidelva.fetch(config)

    print(env.state_config)
    print(env.action_config)

    state = env.reset()
    step, action, terminal = 0, 0, False
    while not terminal and step < FLAGS.max_steps:
        state, reward, terminal, info = env.step(action)
        step += 1

        print(info)

    return 0

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument (
        '--debug', action='store_true',
        help='Turn on debugging information.'
    )

    parser.add_argument (
        '--config', type=str, default='env_configs/stable_noop.json',
        metavar='file', help='Json file with environment config.'
    )

    parser.add_argument (
        '--max_steps', type=int, default=1000, metavar='n',
        help='Max numbers to run environment for.'
    )

    FLAGS = parser.parse_args()
    exit(main(FLAGS))
