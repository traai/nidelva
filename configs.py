#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json

import numpy as np

class DataConfig (object):
    """Data config holds data type and shape."""
    __slots__ = ['_dtype', '_shape']

    # TODO: Want fixed length dtypes?
    # TODO: Want tensorflow dtypes?
    numpy_dtypes = {
        'float' : np.float32,
        'int'   : np.int32
    }

    supported_dtypes = numpy_dtypes.keys()

    @staticmethod
    def dtype_to_numpy (dtype):
        return DataConfig.numpy_dtypes.get(dtype)

    def __init__ (self, dtype, shape):
        self._dtype = dtype
        self._shape = tuple(shape)

    def __repr__ (self):
        return repr(self.to_dict())

    def __str__ (self):
        return str(self.to_dict())

    @property
    def dtype (self):
        return self._dtype

    @property
    def dtype_numpy (self):
        return self.dtype_to_numpy(self.dtype)

    @property
    def shape (self):
        return self._shape

    def to_dict (self):
        return dict(dtype=self.dtype, shape=self.shape)

    @classmethod
    def from_dict (cls, params):
        return cls(**params)

class Config (collections.Mapping):
    """Class for config files."""
    def __init__ (self, *args, **kwargs):
        self.params = dict(*args, **kwargs)

    def __getitem__ (self, key):
        return self.params[key]

    def __iter__ (self):
        return iter(self.params)

    def __len__ (self):
        return len(self.params)

    def __repr__ (self):
        return repr(self.params)

    def __str__ (self):
        return str(self.params)

    def to_file (self, out_file):
        return json.dump(self.params, out_file)

    @classmethod
    def from_file (cls, in_file):
        return cls(json.load(in_file))
