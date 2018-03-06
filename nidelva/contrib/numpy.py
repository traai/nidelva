#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from nidelva import export

import numpy as np

# Import all numpy functions into the np namespace
for key in dir(np):
    value = np.__dict__[key]

    if isinstance(value, np.ufunc):
        export.existing(value, 'np', key)

    if isinstance(value, float):
        export.existing(value, 'np', key)
