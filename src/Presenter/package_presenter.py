#!/usr/bin/python3
from src.IO.XMLParser.output import XMLOutput
from src.Model.Package.package import Package
from src.IO.XMLParser.input import XMLParser
from src.IO.input import Input
from src.Presenter.entry_presenter import EntryPresenter
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class PackagePresenter(Presenter):
    def __init__(self, config):
        self._config=config
        self._entry=None
        self._package = Package(self._config.name)

    @property
    def package(self):
        return self._package


    @property
    def entry(self):
        return self._entry

    @property
    def package_name(self):
        if self.package is not None:
            return self.package.package_name
        return ""

    def load_package(self, language=None):
        # self._package = Package(self._config.name)
        # if language in self._config.available_language:
        #     self._package.language = language

        input_parser=XMLParser(self._config, self._package)
        assert isinstance(input_parser, Input)
        # input_parser.package = self.package
        input_parser.load_package()
        input_parser.load_plugin()
        self._entry=EntryPresenter(self.package.tree)
        return True

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree.content]

    def tab(self, name):
        return self._package.gui_tree.get_tab(name).content

    def save_config(self):
        output = XMLOutput(self._config, self._package)
        try:
            output.write_output()
            return True
        except Exception:
            return False

    def save_native(self):
        output = XMLOutput(self._config, self._package)
        try:
            output.write_native()
            return True
        except Exception:
            return False