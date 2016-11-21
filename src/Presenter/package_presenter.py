#!/usr/bin/python3
from src.IO.XMLParser.output import XMLOutput
from src.Model.Package.package import Package
from src.IO.XMLParser.input import XMLParser
from src.IO.input import Input
from src.Presenter.presenter import Presenter
from src.Presenter.undo_presenter import UndoPresenter

__author__ = 'Ondřej Lanč'


class PackagePresenter(Presenter):
    def __init__(self, config):
        self._config=config
        self._undo = UndoPresenter()
        self._package = Package(self._config.name)
        self._view = None
        self.load_package()

    @property
    def package(self):
        return self._package

    @property
    def undo(self):
        return self._undo

    @property
    def package_name(self):
        if self.package is not None:
            return self.package.name
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
        self.package.tree.init_inconsistency()
        return True

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree.content]

    def tab(self, name):
        if name is None:
            return self._package.gui_tree.first_tab().content
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

    @property
    def tree(self):
        return self._package.tree

    def get_entry(self, path):
        return self.tree.find_entry(path)

    def save_value(self, path, value):
        entry = self.get_entry(path)
        old_value=entry.value
        if value == "":
            value = None
        entry.value = value
        new_value=entry.value
        self._undo.value_change(entry, old_value, new_value)

    def multiple_new(self, path):
        entry = self.get_entry(path)
        newone = entry.append()
        self._undo.multiple_new(entry, newone)
        return newone is not None

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        removed = entry.delete_entry(index)
        self._undo.multiple_delete(entry, removed)
        return removed is not None

    def multiple_up(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_up(index)
        self._undo.multiple_up(entry, index, is_move)
        return is_move

    def multiple_down(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_down(index)
        self._undo.multiple_down(entry, index, is_move)
        return is_move