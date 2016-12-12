#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.lists.constants import Types

__author__ = 'Ondřej Lanč'


class List:
    """Base Class for key_word lists."""

    class Entry:

        def __init__(self, value, label=None, help=None):
            self.value = value
            self.help = help
            self._label = label

        @property
        def label(self):
            return self._label or self.value

        @label.setter
        def label(self, label):
            self._label = label

        def __repr__(self):
            return 'Entry(%s, "%s", "%s")' % (self.value, self.label, self.help)

    def __init__(self, name):
        self._name = name
        self.values = {}

    @property
    def name(self):
        """get name"""
        return self._name

    @name.setter
    def name(self, name):
        """set name"""
        self._name = str(name)

    def append(self, entry):
        self.values[entry.value] = entry

    def contains(self, value):
        """Return True/False if this list contains given value or not."""
        return value in self.values

    @property
    def type(self):
        """Return type of this list entries."""
        return Types.KEY_WORD

    @property
    def entries(self):
        """Return list of entries."""
        return self.values.values()

    def get_entry(self, value):
        """Return entry by value."""
        return self.values.get(value)

    def get_first_entry(self):
        """Return first entry in the list. If there is no entry, return None"""
        if len(self.values) == 0:
            return None
        return self.values[min(self.values.keys())]
