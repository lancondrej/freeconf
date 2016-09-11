#!/usr/bin/python3
#

from src.Model.entries.key_word import KeyWord
from src.Model.entries.multiple.multiple_entry import MultipleEntry

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
