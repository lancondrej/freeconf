#!/usr/bin/python3

import configparser
from os.path import expanduser

from src.Model.Package.package import PackageBase
from src.IO.XMLPackageParser.input import XMLParser
from src.IO.XMLPackageParser.output import XMLOutput
from src.IO.input import Input
from src.IO.output import Output
from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.entry_controller import EntryController

__author__ = 'Ondřej Lanč'


class PackagePresenter(object):
    def __init__(self):
        self._config=ConfigPresenter()
        self._package = None
        self._input = None
        self._output = None

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, package):
        assert isinstance(package, PackageBase)
        self._package=package

    @property
    def packages(self):
        return self._config.packages

    @property
    def package_name(self):
        if self.package is not None:
            return self.package.packageName
        return ""

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

    def load_package(self, name):
        if self.package is not None and self.package.packageName == name:
            return True
        if name not in self.packages:
            return False
        package_conf=self._config.package(name)
        package = PackageBase(name)
        input_parser = XMLParser(package_conf.location)
        output = XMLOutput(package, package_conf.output)
        package.current_language = "en"
        self.package = package
        self.input = input_parser
        self.input.package = self.package
        self.output = output
        self.input.load_package()
        self.input.load_plugins()
        self._entry_controller = EntryController(self.package.tree)
        # del input_parser
        return True

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree._entries]

    def tab(self, name):
        return self._package.gui_tree.get_entry(name).content._entries

    def find_entry(self, path):
        return self.package.tree.find_entry(path)

    def save_value(self, path, value):
        entry = self.find_entry(path)
        entry.value = value


    def multiple_new(self, path):
        entry = self.find_entry(path)
        return entry.create_new()


    def multiple_delete(self, path, index):
        entry = self.find_entry(path)
        return entry.delete_entry(index)


    def multiple_up(self, path, index):
        entry = self.find_entry(path)
        entry.move_up(index)


    def multiple_down(self, path, index):
        entry = self.find_entry(path)
        entry.move_down(index)


    def get_entry(self, path):
        entry = self.find_entry(path)
        return entry

    def save_config(self):
        try:
            self.output.write_output()
            return True
        except Exception:
            return False

    def save_native(self):
        try:
            self.output.write_native()
            return True
        except Exception:
            return False