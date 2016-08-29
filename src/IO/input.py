#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Input():
    def __init__(self):
        self._package = None
        self._source = None

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        self._package = package

    def set_source(self, source):
        self.check_source(source)
        self._source=source

    def check_source(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config_file(self, file):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_plugins(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def input(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @input.setter
    def input(self, input):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError