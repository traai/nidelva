#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from nidelva import export

__all__ = ['Counter']

def _make_callable (obj):
    is_callable = hasattr(obj, '__call__')

    def fn (*args, **kwargs):
        if is_callable:
            return obj(*args, **kwargs)
        return obj
    return fn

@export('class', 'Value')
class Value (object):
    def __init__ (self, initial_value):
        self._initial_value = _make_callable(initial_value)
        self._value = None

    def reset (self):
        self._value = self._initial_value()

    def step (self, *args, **kwargs):
        pass

    @property
    def value (self):
        return self._value

    def __call__ (self):
        return self.value

@export('class', 'Trigger')
class Trigger (Value):
    def __init__ (self, initial_value, trigger_value, condition=True, reset_on_false=False):
        super(Trigger, self).__init__(initial_value)

        self._trigger_value = _make_callable(trigger_value)
        self._condition = _make_callable(condition)
        self._reset_on_false = reset_on_false

    def step (self, *args, **kwargs):
        if self._condition(*args, **kwargs):
            self._value = self._trigger_value(*args, **kwargs)
        elif self._reset_on_false:
            self.reset()

        return self._value

@export('class', 'Counter')
class Counter (Value):
    def __init__ (
            self,
            initial_value, increment,
            lower_limit=None, upper_limit=None,
            condition=True, reset_on_false=False
    ):
        super(Counter, self).__init__(initial_value)

        self._increment = _make_callable(increment)
        self._condition = _make_callable(condition)
        self._reset_on_false = reset_on_false

        self._lower_limit = lower_limit
        self._upper_limit = upper_limit

    def step (self, *args, **kwargs):
        if self._condition(*args, **kwargs):
            self._value += self._increment(*args, **kwargs)
        elif self._reset_on_false:
            self.reset()

        if self._upper_limit is not None:
            self._value = min(self._value, self._upper_limit)
        if self._lower_limit is not None:
            self._value = max(self._value, self._lower_limit)

        return self._value
