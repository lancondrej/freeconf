#!/usr/bin/python3
#
from src.Model.Package.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class BaseEntry(object):
    """This is basis class for all entries."""

    def __init__(self, name, package):
        self._name = name
        self._label = None
        self._parent = None
        self._package = package  # Plugin or package, from which this entry originates.

    def __repr__(self):
        return self.__class__.__name__ + '(' + self.name + ')'

    @property
    def name(self):
        """get name"""
        return self._name

    @name.setter
    def name(self, name):
        """set name"""
        self._name = str(name)

    @property
    def label(self):
        """Returns the correct mutation of the entry's label"""
        return self._label or self.name

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def parent(self):
        """get name"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """set name"""
        self._parent = parent

    @property
    def package(self):
        """get package"""
        return self._package

    @package.setter
    def package(self, package):
        """set package"""
        self._package = package

    @property
    def root(self):
        """Return root of tree."""
        if self.parent:
            return self.parent.root
        return self

    @property
    def full_name(self):
        """Return full path in current tree in form of: /a/b/c/..."""
        path = "/" + self.name
        if self.parent:
            path = self.parent.full_name + path
        return path

