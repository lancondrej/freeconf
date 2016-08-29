#!/usr/bin/python3
#
from copy import deepcopy

from Model.entries.key_word import KeyWord
from Model.entries.multiple.multiple_entry import MultipleEntry
from Model.exception_logging.exception import MultipleError

__author__ = 'Ondřej Lanč'


class MultipleKeyWord(MultipleEntry, KeyWord):
    """Container for multiple config entries."""

    def __init__(self, entry):
        MultipleEntry.__init__(self, entry)

    @property
    def list(self):
        return self.template.list

    @list.setter
    def list(self, l):
        self.template.list=l
