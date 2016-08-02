#!/usr/bin/python3
#
from copy import deepcopy

from Model.constants import Types
from Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'

from Model.entries.base_entry import BaseEntry


class MultipleEntryContainer(BaseEntry):
    """Container for multiple config entries."""

    def __init__(self, entry):
        BaseEntry.__init__(self, entry.name)
        self._parent = entry.parent
        self._entries = []
        self._default = []
        self._template = entry
        self._template.parent=self

    def create_new(self):
        length = self.size()
        if self.multiple_max is None or self.size() < self.multiple_max:
            self._entries.append(deepcopy(self._template))
            self._entries[-1].name=length
            return True
        return False

    def delete_entry(self, index):
        length = self.size()
        if self.multiple_min is None or length > self.multiple_min:
            self._entries.pop(int(index))
            self._rename_all()
            return True
        return False

    def _rename_all(self):
        for i, entry in enumerate(self._entries):
            entry.name=i

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

    def append(self):
        self.create_new()
        return self.entries[-1]

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
        return self._entries

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

    def move_up(self, i):
        """Move given entry up in the list. If it is on the top of the list, nothing happens."""
        i = int(i)
        self._swap(i, i - 1)

    def move_down(self, i):
        """Move given entry down in the list. If it is no the bottom of the list, nothing happens."""
        i = int(i)
        self._swap(i, i + 1)

    @property
    def type(self):
        return Types.MULTIPLE
        #return self._template.type

    def find_entry(self, relative_name):
        """Find entry in tree. Name is given in format: a/b/c../entry"""
        try:
            (number, rest) = relative_name.split('/', 1)
            if self.is_container:
                return self._entries[int(number)].find_entry(rest)
            else:
                return self._entries[int(number)]
        except ValueError:
            pass
        return None