#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.lists.constants import Types
from src.Model.Package.lists.list import List

__author__ = 'Ondřej Lanč'


class StringList(List):
    """Class for string lists.

    :param name: name of list
    """

    class Entry(List.Entry):
        """This class describes particular string for string config keyword.
        It contains string value, optional label and help as an explanation for
        meaning of given string value."""

        def __repr__(self):
            return 'StringEntry(%s, "%s", "%s")' % (
                self.value, self.label, self.help)

    def __init__(self, name):
        List.__init__(self, name)

    @property
    def type(self):
        """Return type of this list entries.

        :return: type of list
        """
        return Types.STRING
