#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class BaseEntry (object):
    """This is basis class for all entries."""
    def __init__(self, name=""):
        self._name = str(name)
        self.parent = None
        self._label = {}
        self._active = True
        self._mandatory = False

        # Multiple properties
        self.multiple = False
        self._multiple_min = None
        self._multiple_max = None

        self._group = None  # Group of entry
        self.package = None  # Plugin or package, from which this entry originates.

    @property
    def name(self):
        """getter"""
        return self._name

    @name.setter
    def name(self, name):
        """setter"""
        self._name = str(name)

    @property
    def root(self):
        """Return root of current tree."""
        obj = self
        while obj.parent is not None:
            obj = obj.parent
        return obj

    def is_section(self):
        """Return true if it is a section."""
        raise NotImplementedError

    def is_keyword(self):
        """Return true if it is a keyword."""
        raise NotImplementedError
