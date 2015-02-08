#!/usr/bin/python3
#
from src.Model.constants import Types

__author__ = 'Ondřej Lanč'


class BaseEntry(object):
    """This is basis class for all entries."""

    def __init__(self, name=""):
        self._name = str(name)
        self.parent = None
        self._active = True
        self._mandatory = False

        # Multiple properties
        self.multiple = False
        self._multiple_min = None
        self._multiple_max = None

    @property
    def name(self):
        """get name"""
        return self._name

    @name.setter
    def name(self, name):
        """set name"""
        self._name = str(name)

    @property
    def root(self):
        """Return root of tree."""
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj

    def is_container(self):
        """Return true if it is a container."""
        raise NotImplementedError

    def is_keyword(self):
        """Return true if it is a keyword."""
        raise NotImplementedError

    @property
    def type(self):
        return Types.UNKNOWN_ENTRY