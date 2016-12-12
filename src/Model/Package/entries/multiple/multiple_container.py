#!/usr/bin/python3
# -*- coding: utf-8 -*-#
from src.Model.Package.entries.multiple.multiple_entry import MultipleEntry

__author__ = 'Ondřej Lanč'


class MultipleContainer(MultipleEntry):
    """Container for multiple config entries."""

    def __init__(self, entry):
        MultipleEntry.__init__(self, entry)
        self._primary = ""

    def add_entry(self, entry):
        return self.template.add_entry(entry)

    def get_entry(self, name):
        return self._template.get_entry(name)

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, primary):
        self._primary=primary

    def primary_value(self, index):
        entry=self.entries[index]
        primary = entry.get_entry(self.primary)
        if primary is not None:
            primary = primary.value
        else:
            primary = index
        return primary
