#!/usr/bin/python3
#
from src.Model.constants import Types
from src.Model.fcfuzzy import FCFuzzy
from src.Model.lists import boolList

__author__ = 'Ondřej Lanč'


class FCBool(FCFuzzy):
    """This is a class for keyword entries of type bool from template file."""

    def __init__(self):
        FCFuzzy.__init__(self)
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

    @property
    def _type_name(self):
        return "BOOL"
