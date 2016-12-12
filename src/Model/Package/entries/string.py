#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re

__author__ = 'Ondřej Lanč'

from src.Model.Package.entries.key_word import KeyWord
from src.Model.Package.lists.constants import Types


class String(KeyWord):
    """This is a class for keyword entries if type string from template file."""

    def __init__(self, name, package):
        KeyWord.__init__(self, name, package)
        self.reg_exp = None

    @property
    def type(self):
        return Types.STRING

    def convert_value(self, value):
        """Check if the given value can be converted to a value for this entry, and if so, return converted value."""
        return str(value)

    def check_value(self):
        """Check if entry's value is within permitted range."""
        if self.value is not None:
            if self.reg_exp is not None:
                return re.match(self.reg_exp, self.value) is not None
        return True

    @property
    def output_value(self):
        """convert value to output string format"""
        if self.value is not None:
            return str(self.value)
