#!/usr/bin/python3
#

__author__ = 'Ondřej Lanč'

from src.Model.base_entry import BaseEntry
from src.Model.constants import Types


class Container(BaseEntry):
    """This is a class for keyword entries from Template File"""

    def __init__(self):
        BaseEntry.__init__(self)
        self._entries = {}

    # Override of functions:
    def is_container(self):
        return True

    def is_keyword(self):
        return False

    def get_entry(self, name):
        """Get entry by name"""
        return self._entries[name]

    def set_entry(self, entry):
        """insert entry at position"""
        assert isinstance(entry, BaseEntry)
        entry.parent = self
        self._entries[entry.name] = entry

    @property
    def entries(self):
        return self._entries

    def size(self):
        return len(self._entries)

    @property
    def type(self):
        return Types.CONTAINER
