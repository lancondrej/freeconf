#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.lists.constants import Types
from src.Model.Package.lists.fuzzy_list import FuzzyList

__author__ = 'Ondřej Lanč'


class BoolList(FuzzyList):
    """Constant fuzzy list of bool values."""

    def __init__(self):
        FuzzyList.__init__(self, "bool")
        # Define bool values
        self.append(FuzzyList.Entry(0.0, "no", "No"))
        self.append(FuzzyList.Entry(1.0, "yes", "Yes"))

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.BOOL


# Create constant list of boolean values
boolList = BoolList()
