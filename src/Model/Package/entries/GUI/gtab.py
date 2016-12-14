#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.Model.Package.entries.GUI.gsection import GSection

__author__ = 'Ondřej Lanč'


class GTab(GSection):
    """GUI tab representation class

    :param name: name of tab
    :param package: package which is tab for
    """

    def __init__(self, name, package):
        GSection.__init__(self, name, package)

    @property
    def sections(self):
        """section getter
        :return: list of section
        """
        return self._entries

    def get_section(self, name):
        """Find entry with given name.

        :return: entry or None
        """
        return self.get_entry(name)
