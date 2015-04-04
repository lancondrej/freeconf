#!/usr/bin/python3
#
from Model.exception_logging.exception import AlreadyExistsError
from Model.multiple_entry_container import MultipleEntryContainer

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
        try:
            return self._entries[name]
        except KeyError:
            return None

    def add_entry(self, entry):
        """insert entry"""
        assert isinstance(entry, BaseEntry)
        if entry.name in self._entries:
            raise AlreadyExistsError(u"Can't add child! There is already entry with name ({s})"
                                     u" in the section ({s}).".format(entry.name, self.name))
        else:
            if entry.multiple:
                # Create multiple container
                entry = MultipleEntryContainer(entry)
                # add multiple entry to the tree
            entry.parent = self
            self._entries[entry.name] = entry
            return True

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
        except KeyError or ValueError:
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
