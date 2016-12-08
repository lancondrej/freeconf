#!/usr/bin/python3
from blinker import signal

from src.IO.XMLParser.output import XMLOutput
from src.Model.Package.entries.GUI.gsection import GSection
from src.Model.Package.entries.GUI.gtab import GTab
from src.Model.Package.entries.entry import Entry
from src.Model.Package.entries.multiple.multiple_entry import MultipleEntry
from src.Model.Package.package import Package
from src.IO.XMLParser.input import XMLParser
from src.IO.input import Input
from src.Presenter.log import logger
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
        self.active_tab = None
        self.inc_signal = signal('inconsistency_change')
        self.load_package()

    @property
    def package(self):
        return self._package

# TODO: lépe výpuis logu
    def undo(self):
        change = self._undo.undo()
        if change is not None:
            self.log("undo entry {}".format(change.entry.name))
            self.view.reload_entry(change.entry)

    def redo(self):
        change = self._undo.redo()
        if change is not None:
            self.log("redo entry {}".format(change.entry.name))
            self.view.reload_entry(change.entry)

    def log(self, message):
        localtime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        logger.debug(message)
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
        self.active_tab = self._package.gui_tree.first_tab()
        self.package.tree.init_inconsistency()
        self.inc_signal.connect(self.test_inc, sender=self.package)
        return True

    @property
    def tabs(self):
        return [(tab.name, tab.label, tab.description, tab.inconsistent) for tab in self._package.gui_tree.tabs]

    def tab(self, name):
        tab = self._package.gui_tree.get_tab(name)
        if tab is not None:
            self.log("change tab from {} to {}".format(self.active_tab.name, name))
            self.active_tab = tab
            self.view.reload_tab(self.active_tab.sections)
        return False

    def save_config(self):
        output = XMLOutput(self._config, self._package)
        if self._package.inconsistent:
            self.view.flash_message('Package is inconsistent.', 'warning')
        try:
            output.write_output()
            self.view.flash_message('Configuration has been saved.', 'success')
        except Exception:
            self.view.flash_message('Configuration can not be save. An error occurred.', 'danger')

    def save_native(self):
        output = XMLOutput(self._config, self._package)
        if self._package.inconsistent:
            self.view.flash_message('Package is inconsistent. Native configuration can not be saved.', 'danger')
        else:
            try:
                output.write_native()
                self.view.flash_message('Native configuration has been saved.', 'success')
            except Exception:
                self.view.flash_message('Native configuration can not be save. An error occurred.', 'danger')

    @property
    def tree(self):
        return self._package.tree

    def get_entry(self, path):
        return self.tree.find_entry(path)

    def save_value(self, path, value):
        entry = self.get_entry(path)
        old_value = entry.value
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
            self.view.flash_message("Cannot add element. Maximum element reach!", 'danger')

    def multiple_delete(self, path, index):
        entry = self.get_entry(path)
        removed = entry.delete_entry(index)
        self._undo.multiple_delete(entry, removed)
        if removed is not None:
            self.log("delete entry for {}".format(removed.full_name))
            self.view.reload_entry(entry)
        else:
            self.view.flash_message("Cannot remove element. Minimum element reach!", 'danger')

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

    def test_inc(self, sender, **kw):
        entry = kw.get('entry')
        if entry is not None:
            if isinstance(entry, GTab):
                self.view.reload_tabs(self.tabs)
            elif isinstance(entry, GSection):
                self.view.reload_section(entry)
            elif isinstance(entry, Entry):
                self.view.reload_entry(entry)

