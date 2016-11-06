#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Input():
    def __init__(self):
        self._package = None

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        self._package = package

    def load_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_header(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_plugins(self, plugins=[]):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError