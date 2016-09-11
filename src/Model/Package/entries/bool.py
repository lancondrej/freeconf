#!/usr/bin/python3
#
from src.Model.Package.lists import boolList

from src.Model.Package.constants import Types
from src.Model.Package.entries.fuzzy import Fuzzy

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
