#!/usr/bin/python3

import configparser
from os.path import expanduser

from Model import PackageBase
from src.IO.input import Input
from src.IO.output import Output
from src.Presenter.entry_controller import EntryController

__author__ = 'Ondřej Lanč'


class Controller(object):
    def __init__(self, package, input, output):
        self.package = package
        self.input = input
        self.input.package = self.package
        self.output = output
        self._freeconf_dirs = []

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        assert isinstance(package, PackageBase)
        self._package=package

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        assert isinstance(input, Input)
        self._input=input

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        assert isinstance(output, Output)
        self._output=output


    def load_config(self, file="config/freeconf.conf"):
        config = configparser.ConfigParser()
        config.read(file)
        self.freeconf_dirs(config["DEFAULT"]["locations"])

    @property
    def freeconf_dirs(self):
        return self._freeconf_dirs

    @freeconf_dirs.setter
    def freeconf_dirs(self, freeconf_dirs):
        for location in freeconf_dirs:
            self._freeconf_dirs.append(expanduser(location))

    def find_packages(self):
        pass

    def load_package(self):
        self.input.load_package()
        self.input.load_plugins()
        self._entry_controller = EntryController(self.package.tree)
        # del input_parser

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree._entries]

    def tab(self, name):
        return self._package.gui_tree.get_entry(name).content._entries

