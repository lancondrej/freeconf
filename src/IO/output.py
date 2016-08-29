#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Output():

    def __init__(self):
        self._package = None

    def write_output(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def write_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def write_native(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def output(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @output.setter
    def output(self, output):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def package(self):
        return self.package

    @package.setter
    def package(self, package):
        self._package = package

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @property
    def native(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @native.setter
    def native(self, native):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError