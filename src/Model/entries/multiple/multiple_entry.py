#!/usr/bin/python3
#
from copy import deepcopy

from Model.constants import Types
from Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'

from Model.entries.base_entry import BaseEntry


class MultipleEntry(BaseEntry):
    """Container for multiple config entries."""

    def __init__(self, entry):
        self._template = entry
        self._template.multiple = True
        self._template.multiple_entry = self
        self._entries = []
        self._default = []
        # Multiple properties
        self._multiple_min = None
        self._multiple_max = None

    @property
    def multiple_max(self):
        return self._multiple_max

    @multiple_max.setter
    def multiple_max(self, value):
        if value > 0:
            self._multiple_max = value
        else:
            # 0 or less means multipleMax property is disabled
            self._multiple_max = None

    @property
    def multiple_min(self):
        return self._multiple_min

    @multiple_min.setter
    def multiple_min(self, value):
        if value > 0:
            self._multiple_min = value
        else:
            # 0 or less means multipleMin property is disabled
            self._multiple_min = None

    @property
    def name(self):
        """get name"""
        return self.template.name

    @name.setter
    def name(self, name):
        """set name"""
        self.template.name(name)

    @property
    def parent(self):
        """get name"""
        return self.template.parent

    @parent.setter
    def parent(self, parent):
        """set name"""
        self.template.parent = parent

    @property
    def package(self):
        """get package"""
        return self.template.package

    @package.setter
    def package(self, package):
        """set package"""
        self.template.package(package)

    @property
    def group(self):
        return self.template.group

    @group.setter
    def group(self, group):
        self.template.group(group)

    @property
    def multiple(self):
        return False

    def create_new(self):
        length = self.size()
        if self.multiple_max is None or self.size() < self.multiple_max:
            self._entries.append(deepcopy(self._template))
            self._entries[-1].index = length
            return self._entries[-1]
        return None

    def delete_entry(self, index):
        length = self.size()
        if self.multiple_min is None or length > self.multiple_min:
            self._entries.pop(int(index))
            self._rename_all()
            return True
        return False

    def _rename_all(self):
        for i, entry in enumerate(self._entries):
            entry.index = i

    def is_container(self):
        return self._template.is_container()

    def is_keyword(self):
        return self._template.is_keyword()

    def is_multiple_entry_container(self):
        return True

    def get_multiple_entry(self, i):
        return self._entries[i]

    def insert_multiple_entry(self, entry, position):
        # assert isinstance(entry, BaseEntry)
        # entry.parent = self
        self._entries.insert(int(position), entry)

    def append(self):
        self.create_new()
        return self.entries[-1]

    def append_default(self, entry):
        if entry is not None:
            # assert isinstance(entry, BaseEntry)
            # entry.parent = self
            self._default.append(entry)
            return entry

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
            self._rename_all()

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
        # return Types.MULTIPLE
        return self.template.type

    def find_entry(self, relative_name):
        """Find entry in tree. Name is given in format: a/b/c../entry"""
        try:
            (number, rest) = relative_name.split('/', 1)
            if self.is_container:
                return self._entries[int(number)].find_entry(rest)
        except ValueError:
            return self._entries[int(relative_name)]
        return None


