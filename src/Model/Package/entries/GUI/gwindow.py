#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GWindow(GSection):
    """Class that represents the top-level dialogue window

    :param name: name of window
    :param package: package which is window for
    """

    def __init__(self, name, package):
        GSection.__init__(self, name, package)

    @property
    def tabs(self):
        """tabs getter

        :return: list of tabs
        """
        return self._entries

    def get_tab(self, name):
        """Find tab with given name.

        :param name: name of tab
        :return: tab or None
        """
        return self.get_entry(name)

    def first_tab(self):
        """Find tab with given name.

        :return: entry or None
        """
        return self._entries[0]
