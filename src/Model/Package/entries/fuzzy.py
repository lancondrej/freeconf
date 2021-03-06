#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.Model.Package.entries.key_word import KeyWord
from src.Model.Package.lists.constants import Types
from src.Model.exception import ModelGeneralException

__author__ = 'Ondřej Lanč'


class Fuzzy(KeyWord):
    """This is a class for keyword entries of type fuzzy."""

    def __init__(self, name, package):
        KeyWord.__init__(self, name, package)
        # # Initialize Properties
        # Maximum possible value
        self._max = 1.0
        # Minimum possible value
        self._min = 0.0

    @property
    def type(self):
        return Types.FUZZY

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @max.setter
    def max(self, m):
        assert type(m) == float and 0.0 <= m <= 1.0
        self._max = m

    @min.setter
    def min(self, m):
        assert type(m) == float and 0.0 <= m <= 1.0
        self._min = m

    def value_to_grade(self, value):
        """Return grade for given value."""
        if value is None:
            return None
        entry = self.list.get_entry(value)
        if entry is not None:
            return entry.grade
        else:
            return None

    def grade_to_value(self, grade):
        """Return valid value from fuzzy list with given grade."""
        if grade is None:
            return None
        else:
            # Find value with given grade
            entry = self.list.get_exact_grade(grade)
            if entry is None:
                raise ModelGeneralException(
                    "Value with grade %d was not found in fuzzy list %s!" % (
                    grade, self.list.name))
            return entry.value

    @property
    def default_grade(self):
        """Get grade of default value."""
        return self.value_to_grade(self.default_value)

    @default_grade.setter
    def default_grade(self, grade):
        """Set default value with given grade."""
        self.default_value = self.grade_to_value(grade)

    def convert_value(self, value):
        """Check if given value can be converted to value for this entry, and if so, return converted value."""
        value = str(value)
        return value

    def check_value(self):
        """Check if entry's value is within permitted range."""
        if self.value is not None:
            entry = self.list.get_entry(self.value)
            if entry is not None:
                if entry.grade > self.max:
                    return False
                if entry.grade < self.min:
                    return False
                return True
        return False

    @property
    def grade(self):
        return self.value_to_grade(self.value)

    @grade.setter
    def grade(self, grade):
        self.value = self.grade_to_value(grade)

    @property
    def output_value(self):
        """convert value to output string format"""
        if self.value is not None:
            return str(self.value)
