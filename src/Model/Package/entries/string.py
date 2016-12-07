#!/usr/bin/python3
#

__author__ = 'Ondřej Lanč'

from src.Model.Package.entries.key_word import KeyWord
from src.Model.Package.lists.constants import Types


class String(KeyWord):
    """This is a class for keyword entries if type string from template file."""

    def __init__(self, name, package):
        KeyWord.__init__(self, name, package)
        self.reg_exp = ""

    @property
    def type(self):
        return Types.STRING

    def convert_value(self, value):
        """Check if the given value can be converted to a value for this entry, and if so, return converted value."""
        return str(value)

    def check_value(self):
        """Check if entry's value is within permitted range."""
        return True