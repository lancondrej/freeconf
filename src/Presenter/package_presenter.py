#!/usr/bin/python3
from src.IO.XMLParser.output import XMLOutput
from src.Model.Package.package import Package
from src.IO.XMLParser.input import XMLParser
from src.IO.input import Input
from src.Presenter.presenter import Presenter
from src.Presenter.undo_presenter import UndoPresenter
import time

__author__ = 'Ondřej Lanč'


class PackagePresenter(Presenter):
    def __init__(self, config):
        self._config=config
        self._undo = UndoPresenter()
        self._package = Package(self._config.name)
        self.view = None
        self.load_package()

    @property
    def package(self):
        return self._package

# TODO: lépe výpuis logu
    def undo(self):
        change = self._undo.undo()
        if change is not None:
            self.log("redo entry {}".format(change.entry.name))
            self.view.reload_entry(change.entry)

    def redo(self):
        change = self._undo.redo()
        if change is not None:
            self.log("redo entry {}".format(change.entry.name))
            self.view.reload_entry(change.entry)

    def log(self, message):
        localtime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        self.view.log(localtime, message)

    @property
    def package_name(self):
        if self.package is not None:
            return self.package.name
        return ""

    def load_package(self, language=None):
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
            self.view.flash_message('Configuration save', 'success')
        except Exception:
            self.view.flash_message('Configuration not save', 'danger')

    def save_native(self):
        output = XMLOutput(self._config, self._package)
        try:
            output.write_native()
            self.view.flash_message('Native configuration save', 'success')
        except Exception:
            self.view.flash_message('Native Configuration not save', 'danger')

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
        self.log("{} key word change value from {} to {}".format(entry.name, old_value, new_value))

    def multiple_new(self, path):
        entry = self.get_entry(path)
        newone = entry.append()
        self._undo.multiple_new(entry, newone)
        if newone is not None:
            self.log("delete entry for {}".format(newone.full_name))
            self.view.reload_entry(entry)
        else:
            self.view.flash_message("Cannot add element. Maximum element reach!", 'error')

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        removed = entry.delete_entry(index)
        self._undo.multiple_delete(entry, removed)
        if removed is not None:
            self.log("delete entry for {}".format(removed.full_name))
            self.view.reload_entry(entry)
        else:
            self.view.flash_message("Cannot remove element. Minimum element reach!", 'error')

    def multiple_up(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_up(index)
        self._undo.multiple_up(entry, index, is_move)
        if is_move:
            self.log("entry move up")
            self.view.reload_entry(entry)

    def multiple_down(self, path, index):
        entry = self.get_entry(path)
        is_move = entry.move_down(index)
        self._undo.multiple_down(entry, index, is_move)
        if is_move:
            self.log("entry move down")
            self.view.reload_entry(entry)

