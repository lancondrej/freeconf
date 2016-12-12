#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.Model.Package.lists.constants import Types
from src.Model.Package.lists.list import List

__author__ = 'Ondřej Lanč'


class FuzzyList(List):
    """Class for fuzzy lists."""

    class Entry(List.Entry):
        """This class describes particular value for fuzzy config keyword."""

        def __init__(self, grade, value, label=None, help=None):
            assert 0 <= grade <= 1
            self.grade = grade
            List.Entry.__init__(self, value, label, help)

        def __repr__(self):
            return 'FuzzyEntry(%s, "%s", "%s")' % (self.value, self.label, self.help)

    def __init__(self, name):
        List.__init__(self, name)

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.FUZZY

    def get_exact_grade(self, grade):
        """Return entry with given grade. If such entry is not found, None is returned."""
        for e in self.values.values():
            if e.grade == grade:
                return e
        return None

    def get_max_grade(self, max_grade=1.0):
        """Return entry with maximum grade that is lower or equal than maxGrade."""
        max_entry = None
        for e in self.values.values():
            if e.grade <= max_grade and (max_entry is None or max_entry.grade < e.grade):
                max_entry = e
        return max_entry

    def get_min_grade(self, min_grade=0.0):
        """Return entry with minimum grade that is higher or equal than minGrade."""
        min_entry = None
        for e in self.values.values():
            if e.grade >= min_grade and (min_entry is None or min_entry.grade > e.grade):
                min_entry = e
        return min_entry

    def join_list(self, new_list):
        """Add new value list to this fuzzy list."""
        for key in new_list.values:
            if not key in self.values:
                self.values[key] = new_list.values[key]
            else:
                # Key is already in the list. Check if it has same grade
                if new_list.values[key].grade != self.values[key].grade:
                    raise Exception
                    # self.logger.error("FcFuzzyList: joinList: Joining %s with %s. "
                    #           "Value '%s' is already in the list but with"
                    #           " different grade!" % (self.name, new_list.name, key))
        return self



