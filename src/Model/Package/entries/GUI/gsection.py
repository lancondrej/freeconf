#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.entries.base_entry import BaseEntry
from src.Model.Package.inconsistency import ContainerInconsistency

__author__ = 'Ondřej Lanč'


class GSection(BaseEntry, ContainerInconsistency):
    """GUI container class"""
    def __init__(self, name, package):
        BaseEntry.__init__(self, name, package)
        self._inc_parents = set()
        self.parent = None
        self.description = None

        ContainerInconsistency.__init__(self)
        # self._active_shown = 0
        # self._mandatory_shown = 0
        # self._section_shown = 0
        # self.empty = None
        # self._show_all_children = False
        self._entries = []


    @property
    def inc_parents(self):
        return self._inc_parents

    @property
    def entries(self):
        return self._entries

    #
    # @property
    # def show_all_children(self):
    #     return self._show_all_children

    # @property
    # def primaryChildName(self):
    #     raise AttributeError("Property primaryChildName is write only!")
    #
    # @primaryChildName.setter
    # def primaryChildName(self, name):
    #     self._primaryChildName = name
    #     self._primaryChild = None

    def append(self, entry):
        entry.inc_parents.add(self)
        self._entries.append(entry)

    def get_entry(self, name):
        """Find entry with given name."""
        indices = [i for i, x in enumerate(self._entries) if x.name == name]
        if len(indices) == 0:
            return None
        else:
            return self._entries[indices[0]]
