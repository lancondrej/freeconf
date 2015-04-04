#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Input():

    def load_package(self, package):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config_file(self, file, package):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_plugins(self, package):
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