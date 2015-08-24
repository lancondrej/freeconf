#!/usr/bin/python3
#

__author__ = 'Ondřej Lanč'

from Model.key_word import KeyWord
from Model.constants import Types


class String(KeyWord):
    """This is a class for keyword entries if type string from template file."""

    def __init__(self):
        KeyWord.__init__(self)
        self.regExp = ""

    @property
    def type(self):
        return Types.STRING

    @property
    def _type_name(self):
        return "STRING"

    def convert_value(self, value):
        """Check if the given value can be converted to a value for this entry, and if so, return converted value."""
        assert type(value) is str
        return value