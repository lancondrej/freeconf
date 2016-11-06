#!/usr/bin/python3

from src.Model.Package.package import Package
from src.IO.XMLPackageParser.input import XMLParser
from src.IO.input import Input
from src.Presenter.entry_presenter import EntryPresenter
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class PackagePresenter(Presenter):
    def __init__(self, config):
        self._config=config
        self._entry=None
        self._package = None

    @property
    def package(self):
        return self._package


    @property
    def entry(self):
        return self._entry

    # @package.setter
    # def package(self, package):
    #     assert isinstance(package, PackageBase)
    #     self._package=package

    @property
    def available_packages(self):
        return self._config.package_list

    @property
    def package_name(self):
        if self.package is not None:
            return self.package.package_name
        return ""

    def load_package(self, language=None):
        self._package = Package(self._config.name)
        if language in self._config.avaiable_language:
            self._package.current_language = language
        else:
            self._package.current_language = self._config.default_language

        input_parser=XMLParser(self._config.location)
        assert isinstance(input_parser, Input)
        input_parser.package = self.package
        input_parser.location = self._config.location
        input_parser.load_package()
        input_parser.load_plugins()

        self._entry=EntryPresenter(self.package.tree)
        # output = XMLOutput(self.package, self._config.output, self._config.native, self._config.xslt)
        # self.output = output
        # self.input.load_package()
        # self.input.load_plugins()
        # self._entry_controller = EntryController(self.package.tree)
        # del input_parser
        return True

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree._entries]

    def tab(self, name):
        return self._package.gui_tree.get_entry(name).content._entries

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