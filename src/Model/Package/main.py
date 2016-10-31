#!/usr/bin/python3

__author__ = 'Ondřej Lanč'


from src.Model.Package.package import Package


class FreeconfModel(object):
    """Base class for Freeconf Model structure."""

    def __init__(self):
        self._freeconf_dirs = []
        self._languages = []
        self._package = None

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        assert isinstance(package, Package)
        self._package = package

    @property
    def freeconf_dirs(self):
        return self._freeconf_dirs

    @freeconf_dirs.setter
    def freeconf_dirs(self, dirs):
        self._freeconf_dirs = dirs

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, langs):
        self._languages = langs
