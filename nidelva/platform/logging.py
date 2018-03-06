#! /usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#FIXME: This entire module

import logging

DEBUG = logging.DEBUG
ERROR = logging.ERROR
FATAL = logging.FATAL
INFO = logging.INFO
WARN = logging.WARN

def get_logger (name):
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt=logging.BASIC_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

logger = get_logger('nidelva')

debug = logger.debug
error = logger.error
fatal = logger.fatal
info = logger.info
warn = logger.warn

def get_verbosity ():
    return logger.getEffectiveLevel()

def set_verbosity (level):
    return logger.setLevel(level)
