#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import configs
import environments
import Simulator

def main ():
    # Rough usage sketch
    simulator = Simulator.Simulator()

    with open('env_configs/simple_customer.json', 'r') as in_file:
        config = configs.Config.from_file(in_file)

    simulator = simulator.load_config(config)
    environment = simulator.build_environment()

    # TODO: convenience function?
    # environment = Simulator.load_file_and_build('env_configs/simple_customer.json')

    print(environment.state_config)
    print(environment.action_config)

    state = environment.reset()
    terminal = False
    while not terminal:
        action = 0

        state, reward, terminal, info = environment.step(action)
        print('state={}, reward={}, terminal={}'.format(state, reward, terminal))
        # print('info={}'.format(info))

    return 0

if __name__ == '__main__':
    exit(main())
