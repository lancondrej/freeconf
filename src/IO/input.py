#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Input(object):

    def load_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_plugin(self, plugins=None):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError