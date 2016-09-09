#!/usr/bin/python3
#
from src.Model.constants import Types
from src.Model.entries.fuzzy import Fuzzy
from src.Model.lists import boolList

__author__ = 'Ondřej Lanč'


class Bool(Fuzzy):
    """This is a class for keyword entries of type bool from template file."""

    def __init__(self):
        Fuzzy.__init__(self)
        self.list = boolList

    @property
    def type(self):
        return Types.BOOL

    # Min and Max properties are read-only in this class
    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max
