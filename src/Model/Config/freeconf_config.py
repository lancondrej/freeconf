#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Ondřej Lanč'


class Config(object):
    """Config model object. Store information of Freeconf at all.
     Information about all packages and lang preferences.
    """
    def __init__(self):
        self._config_file = "freeconf.xml"
        self._packages = {}
        self._lang = None

    @property
    def packages(self):
        """ packages getter
            :return dict: packages dictionary
        """
        return self._packages

    def package(self, name):
        """ package getter
            :param name: name of package
            :return Package or None
        """
        return self._packages[name]

    @property
    def config_file(self):
        """ config_file getter
            :return path of config file
        """
        return self._config_file

    @property
    def lang(self):
        """ lang getter
            :return lang code
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """lang setter
            :param lang - lang code"""
        self._lang=lang
