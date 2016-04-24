#!/usr/bin/python3
#
from Model.constants import Types
from Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'

from Model.base_entry import BaseEntry


class MultipleEntryContainer(BaseEntry):
    """Container for multiple config entries."""

    def __init__(self, entry):
        BaseEntry.__init__(self, entry.name)
        self._parent = entry.parent
        self._entries = []
        self._default = []
        self._template = entry

    def make_entry(self):
        pass

    def is_container(self):
        if self._template.is_container():
            return True
        return False

    def is_keyword(self):
        if self._template.is_keyword():
            return True
        return False

    def is_multiple_entry_container(self):
        return True

    def get_multiple_entry(self, i):
        return self._entries[i]

    def insert_multiple_entry(self, entry, position):
        # assert isinstance(entry, BaseEntry)
        entry.parent = self
        self._entries.insert(int(position), entry)

    def append(self, entry):
        if entry is not None:
            # assert isinstance(entry, BaseEntry)
            entry.parent = self
            self._entries.append(entry)
            return entry

    def append_default(self, entry):
        if entry is not None:
            # assert isinstance(entry, BaseEntry)
            entry.parent = self
            self._default.append(entry)
            return entry

    def add_entry(self, entry):
        if self._template.is_container() or self._template.is_multiple_entry_container():
            self._template.add_entry(entry)
        raise MultipleError("Add entry - Multiple container is not container.")

    def get_entry(self, name):
        if self._template.is_container():
            return self._template.get_entry(name)
        raise MultipleError("get entry - Multiple container is not container.")

    def disconnect(self, entry):
        try:
            self._entries.remove(entry)
            entry.parent = None
            return True
        except ValueError as KeyError:
            return False

    @property
    def entries(self):
        entries ={}
        i=0
        for entry in self._entries:
            entries[entry.name+str(i)] = entry.entries
            i=i+1
        return entries

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template_entry):
        self._template = template_entry

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

    @property
    def type(self):
        return Types.MULTIPLE
        #return self._template.type