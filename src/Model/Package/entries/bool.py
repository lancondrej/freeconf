#!/usr/bin/python3
# -*- coding: utf-8 -*-#
from src.Model.Package.entries.fuzzy import Fuzzy
from src.Model.Package.lists.bool_list import boolList
from src.Model.Package.lists.constants import Types

__author__ = 'Ondřej Lanč'


class Bool(Fuzzy):
    """This is a class for keyword entries of type bool from template file."""

    def __init__(self, name, package):
        Fuzzy.__init__(self, name, package)
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
