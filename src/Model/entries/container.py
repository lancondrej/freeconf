#!/usr/bin/python3
#


__author__ = 'Ondřej Lanč'

from src.Model.constants import Types
from src.Model.entries.base_entry import BaseEntry
from src.Model.exception_logging.exception import AlreadyExistsError
from copy import deepcopy,copy

class Container(BaseEntry):
    """This is a class for keyword entries from Template File"""

    def is_multiple_entry_container(self):
        return False

    def __init__(self):
        BaseEntry.__init__(self)
        self._entries = {}

    def __deepcopy__(self, memo):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        newone._entries = deepcopy(self._entries)
        for entry in newone._entries.values():
            entry.parent=newone
        return newone

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
        # assert isinstance(entry, BaseEntry)
        if entry.name in self._entries:
            raise AlreadyExistsError(u"Can't add child! There is already entry with name ({s})"
                                     u" in the section ({s}).".format(entry.name, self.name))
        # elif isinstance(entry, BaseEntry):
            # if entry.multiple:
            #     # Create multiple container
            #     entry = MultipleEntryContainer(entry)
            #     # add multiple entry to the tree
        entry.parent = self
        self._entries[entry.name] = entry
        return True

    @property
    def entries(self):
        return self._entries\

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
            (name, rest) = relative_name.split('/', 1)
            if relative_name.startswith('/'):
                (name, rest) = rest.split('/', 1)
                if self.root.name == name:
                    return self.root.find_entry(rest)
            if self.is_in_container(name):
                return self.get_entry(name).find_entry(rest)
        except ValueError:
            if self.is_in_container(relative_name):
                return self.get_entry(relative_name)
        return None

    # # @property
    # def primary(self):
    #     if self.multiple:
    #         primary = self.get_entry(self.multiple_entry.primary)
    #         if primary:
    #             primary = primary.value
    #         else:
    #             primary = self.index
    #         return primary
    #     return None