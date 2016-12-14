#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.Model.Package.lists.constants import Types
from src.Model.Package.lists.list import List

__author__ = 'Ondřej Lanč'


class FuzzyList(List):
    """Class for fuzzy lists.

    :param name: name of list
    """

    class Entry(List.Entry):
        """This class describes particular value for fuzzy config keyword.

        :param grade: grage of fuzzy entry
        :param value: entry value
        :param label: entry label
        :param help: entry help
        """

        def __init__(self, grade, value, label=None, help=None):

            assert 0 <= grade <= 1
            self.grade = grade
            List.Entry.__init__(self, value, label, help)

        def __repr__(self):
            return 'FuzzyEntry(%s, "%s", "%s")' % (
                self.value, self.label, self.help)

    def __init__(self, name):
        List.__init__(self, name)

    @property
    def type(self):
        """Return type of this list entries.

        :return: type of list
        """
        return Types.FUZZY

    def join_list(self, new_list):
        """Add new value list to this fuzzy list.

        :param new_list: list to merge
        """
        for key in new_list.values:
            if not key in self.values:
                self.values[key] = new_list.values[key]
            else:
                # Key is already in the list. Check if it has same grade
                if new_list.values[key].grade != self.values[key].grade:
                    from src.Model.exception import AlreadyExistsException
                    raise AlreadyExistsException(
                        "Joining {} with {}. Value '{}' is "
                        "already in the list but with different"
                        " grade!".format((self.name, new_list.name, key)))
        return self
