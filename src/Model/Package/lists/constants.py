#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum

__author__ = 'Ondřej Lanč'


class Types(Enum):
    """Basic Freeconf types. Now Used in lists."""
    # # Entry Types ##
    KEY_WORD = 1
    FUZZY = 2
    BOOL = 3
    NUMBER = 4
    STRING = 5
