#!/usr/bin/python3
#

__author__ = 'Ondřej Lanč'

from src.Model.base_entry import BaseEntry
from src.Model.constants import Types


class Container(BaseEntry):
    """This is a class for keyword entries from Template File"""

    def is_multiple_entry_container(self):
        return False

    def __init__(self):
        BaseEntry.__init__(self)
        self._entries = {}

    # Override of functions:
    def is_container(self):
        return True

    def is_keyword(self):
        return False

    def is_in_container(self, name):
        return name in self._entries

    def get_entry(self, name):
        """Get entry by name"""
        return self._entries[name]

    def add_entry(self, entry):
        """insert entry"""
        assert isinstance(entry, BaseEntry)
        if entry.name not in self._entries:
            entry.parent = self
            self._entries[entry.name] = entry
            return True
        return False

    @property
    def entries(self):
        return self._entries

    def size(self):
        return len(self._entries)

    @property
    def type(self):
        return Types.CONTAINER

    def disconnect(self, entry):
        try:
            self._entries.pop(entry.name)
            entry.parent = None
            return True
        except ValueError as KeyError:
            return False

    def find_entry(self, relative_name):
        """Find entry in tree. Name is given in format: a/b/c../entry"""
        try:
            (name, rest) = relative_name.split('/',1)
            if self.is_in_container(name):
                return self.find_entry(rest)
        except ValueError:
            if self.is_in_container(relative_name):
                return self.get_entry(relative_name)
        return None