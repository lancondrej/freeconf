#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


class Output():

    def __init__(self):
        self._package = None

    def write_output(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def write_native(self, groups=None):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError
