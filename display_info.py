#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import numpy as np

from matplotlib import pyplot as plt

def process_file (in_file):
    values = {}

    for line in in_file:
        line = line.replace('\'', '"')
        info = json.loads(line)

        for key in info:
            if key not in values:
                values[key] = []

            values[key].append(info[key])

    return values

def main (FLAGS):
    with open(FLAGS.info_file, 'r') as in_file:
        values = process_file(in_file)

    plt.plot(values['step_counter'], values['usage'], label='usage')
    plt.plot(values['step_counter'], values['quota'], label='quota')
    plt.ylim(0, None)
    plt.legend()
    plt.show()
    return 0

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument (
        'info_file', type=str, metavar='file',
        help='Info dump file.'
    )

    FLAGS = parser.parse_args()
    exit(main(FLAGS))
