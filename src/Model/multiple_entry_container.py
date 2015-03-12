#!/usr/bin/python3
#
from src.Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'

from src.Model.base_entry import BaseEntry
from src.Model.exception_logging.log import log


class MultipleEntryContainer(BaseEntry):
    """Container for multiple config entries."""

    def __init__(self, name, parent):
        BaseEntry.__init__(self, name)
        self.parent = parent
        self._entries = []

    def make_entry(self):
        pass

    def is_container(self):
        False

    def is_keyword(self):
        False

    def is_multiple_entry_container(self):
        return True

    def get_entry(self, i):
        return self._entries[i]

    def insert_entry(self, entry, position):
        # assert isinstance(entry, BaseEntry)
        entry.parent = self
        self._entries.insert(int(position), entry)

    def append(self, entry):
        if entry is not None:
            # assert isinstance(entry, BaseEntry)
            entry.parent = self
            self._entries.append(entry)

    def replace_entry(self, old, new):
        (index, node) = self.findEntry(old)
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
        if i != j:
            (self._entries[i], self._entries[j]) = (self._entries[j], self._entries[i])

    def move_up(self, entry):
        """Move given entry up in the list. If it is on the top of the list, nothing happens."""
        i = self._entries.index(entry)
        self._swap(i, i - 1)

    def move_down(self, entry):
        """Move given entry down in the list. If it is no the bottom of the list, nothing happens."""
        i = self._entries.index(entry)
        self._swap(i, i + 1)