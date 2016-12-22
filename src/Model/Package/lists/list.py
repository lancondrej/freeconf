#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.lists.constants import Types

__author__ = 'Ondřej Lanč'


class List:
    """Base Class for key_word lists.

    :param name: name of list
    """

    class Entry:
        """Base entry for lists

        :param value: entry value
        :param label: entry label
        :param help: entry help
        """
        def __init__(self, value, label=None, help=None):
            self.value = value
            self.help = help
            self._label = label

        @property
        def label(self):
            """label getter

            :return: label or value
            """
            return self._label or self.value

        @label.setter
        def label(self, label):
            """lable setter

            :param label:
            """
            self._label = label

        def __repr__(self):
            return 'Entry(%s, "%s", "%s")' % (
            self.value, self.label, self.help)

    def __init__(self, name):
        self._name = name
        self.values = {}

    @property
    def name(self):
        """name getter

        :return: name
        """
        return self._name

    @name.setter
    def name(self, name):
        """name setter

        :param name: name of list
        """
        self._name = str(name)

    def append(self, entry):
        """append entry to list

        :param entry:
        """
        self.values[entry.value] = entry

    def contains(self, value):
        """Return True/False if this list contains given value or not.

        return: bool
        """
        return value in self.values

    @property
    def type(self):
        """Return type of this list entries.

        :return: type of list
        """
        return Types.KEY_WORD

    @property
    def entries(self):
        """Return list of entries.

        :return: list of list entries
        """
        return self.values.values()

    def get_entry(self, value):
        """Return entry by value.

        :param value: valeu of entry
        :return: entry or None
        """
        return self.values.get(value)

    def get_first_entry(self):
        """Return first entry in the list. If there is no entry, return None

        :return: entry or None
        """
        if len(self.values) == 0:
            return None
        return self.values[min(self.values.keys())]

    def join_list(self, new_list):
        """Add new value list to this list.

        :param new_list: list to merge
        """
        for key in new_list.values:
            if key not in self.values:
                self.values[key] = new_list.values[key]
        return self
