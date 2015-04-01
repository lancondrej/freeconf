#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Input():

    def load_package(self, package, load_languages):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config_file(self, package):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_plugins(self, package, load_languages):
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

    @property
    def config(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    @config.setter
    def config(self, config):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError