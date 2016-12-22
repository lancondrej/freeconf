#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.entries.base_entry import BaseEntry
from src.Model.Package.inconsistency import ContainerInconsistency

__author__ = 'Ondřej Lanč'


class GSection(BaseEntry, ContainerInconsistency):
    """GUI section class

    :param name: name of section
    :param package: package which is section for
    """

    def __init__(self, name, package):
        BaseEntry.__init__(self, name, package)
        self.parent = None
        self.description = None

        ContainerInconsistency.__init__(self)
        self._entries = []

    @property
    def entries(self):
        """entries getter

        :return:  entries
        """
        return self._entries

    def append(self, entry):
        """append entry into section

        :param entry:
        """
        entry.inc_parents.add(self)
        self._entries.append(entry)

    def get_entry(self, name):
        """Find entry with given name.

        :return: entry or None
        """
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._entries[indices[0]]
