#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Ondřej Lanč'


class Output(object):
    def write_output(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def write_native(self, groups=None):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError
