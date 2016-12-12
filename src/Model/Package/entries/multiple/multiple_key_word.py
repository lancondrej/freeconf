#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from src.Model.Package.entries.multiple.multiple_entry import MultipleEntry

__author__ = 'Ondřej Lanč'


class MultipleKeyWord(MultipleEntry):
    """Container for multiple config entries."""

    def __init__(self, entry):
        MultipleEntry.__init__(self, entry)

    @property
    def list(self):
        return self.template.list

    @list.setter
    def list(self, l):
        self.template.list=l

    @property
    def static_mandatory(self):
        return self.template.static_mandatory

    @static_mandatory.setter
    def static_mandatory(self, mandatory):
        self.template.static_mandatory = mandatory