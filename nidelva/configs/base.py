#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from nidelva import export

__all__ = ['DataConfig', 'Shape']

@export('config', 'Shape')
class Shape (tuple):
    def as_list (self):
        return list(self)

    def as_batch (self):
        return type(self)([None] + self.as_list()[1:])

    def prod (self):
        return reduce(lambda x,y : x*y, self, 1)

@export('config', 'Data')
class DataConfig (object):
    """Data config holds data type and shape."""
    __slots__ = ['_dtype', '_shape']

    numpy_dtypes = {
        # Common
        'float' : np.float32,
        'int'   : np.int32,
        'uint'  : np.uint32,

        # Fixed size floats
        'float16' : np.float16,
        'float32' : np.float32,
        'float64' : np.float64,

        'half'   : np.float16,
        'single' : np.float32,
        'double' : np.float64,

        # Fixed size signed ints
        'int8'  : np.int8,
        'int16' : np.int16,
        'int32' : np.int32,
        'int64' : np.int64,

        'byte'  : np.int8,
        'char'  : np.int8,
        'word'  : np.int16,
        'dword' : np.int32,
        'qword' : np.int64,

        # Fixed sized unsigned ints
        'uint8'  : np.uint8,
        'uint16' : np.uint16,
        'uint32' : np.uint32,
        'uint64' : np.uint64,
    }

    supported_dtypes = numpy_dtypes.keys()

    @staticmethod
    def dtype_to_numpy (dtype):
        return DataConfig.numpy_dtypes.get(dtype)

    def __init__ (self, dtype, shape):
        self._dtype = dtype
        self._shape = Shape(shape)

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

    def with_shape (self, shape):
        return type(self)(dtype=self.dtype, shape=shape)

    def with_dtype (self, dtype):
        return type(self)(dtype=dtype, shape=self.shape)

    def as_batch (self):
        return type(self)(dtype=self.dtype, shape=self.shape.as_batch())

    def to_dict (self):
        return dict(dtype=self.dtype, shape=self.shape)

    @classmethod
    def from_dict (cls, params):
        return cls(**params)
