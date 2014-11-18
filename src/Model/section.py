#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

from src.Model.base_entry import BaseEntry


class Section(BaseEntry):
    """This is a class for keyword entries from Template File"""

    def __init__(self):
        BaseEntry.__init__(self)
        self._entries = []

    # Override of functions:
    def is_section(self):
        return True

    def is_keyword(self):
        return False

    def get_entry(self, i):
        """Get entry by index"""
        return self._entries[i]

    def find_entry(self, name):
        """Find (first) entry with given name."""
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None, None
        else:
            return indices[0], self._entries[indices[0]]

    def insert_entry(self, entry, position):
        """insert entry at position"""
        #assert isinstance(entry, BaseEntry)
        entry.parent = self
        self._entries.insert(int(position), entry)

    def append(self, entry):
        if entry is not None:
            #assert isinstance(entry, BaseEntry)
            entry.parent = self
            self._entries.append(entry)

    def replace_entry(self, old, new):
        (index, node) = self.find_entry(old)
        if index is None:
            return False
        self._entries[index] = new
        new.parent = self
        return True

    def disconnect(self, entry):
        try:
            self._entries.remove(entry)
            entry.parent = None
            return True
        except ValueError as KeyError:
            return False

    @property
    def entries(self):
        return self._entries

    def size(self):
        return len(self._entries)

    def _swap(self, i, j):
        """Swap entries at given positions."""
        # Check range
        i = min(self.size() - 1, max(0, i))
        j = min(self.size() - 1, max(0, j))
        if i == j:
            return
        # Swap entries
        self._entries[i], self._entries[j] = self._entries[j], self._entries[i]

    def move_up(self, entry):
        """Move given entry up in the list. If it is on the top of the list, nothing happens."""
        i = self._entries.index(entry)
        self._swap(i, i - 1)

    def move_down(self, entry):
        """Move given entry down in the list. If it is no the bottom of the list, nothing happens."""
        i = self._entries.index(entry)
        self._swap(i, i + 1)