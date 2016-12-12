#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GWindow(GSection):
    """Class that represents the top-level dialogue window"""
    def __init__(self, name, package):
        GSection.__init__(self, name, package)
        self.label = "Freeconf generated config dialog"

    # def show_all (self, value):
    #     for tab in self.entries:
    #         tab.show_all(value)

    @property
    def tabs(self):
        return self._entries

    def get_tab(self, name):
        """Find tab with given name."""
        return self.get_entry(name)

    def first_tab(self):
        """Find tab with given name."""
        return self._entries[0]
