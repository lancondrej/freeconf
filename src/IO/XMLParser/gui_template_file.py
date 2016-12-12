#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.IO.XMLParser.file import FileReader
from src.Model.Package.entries.GUI.gsection import GSection
from src.Model.Package.entries.GUI.gtab import GTab
from src.Model.Package.entries.GUI.gwindow import GWindow
from src.Model.Package.package import Plugin

__author__ = 'Ondřej Lanč'


class GUITemplateFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        gui_template_file = self._config.gui_template_file
        super().__init__(gui_template_file)
        self.logger.info("Loading GUI template file {}".format(
            gui_template_file))

    def parse(self):
        if isinstance(self._package, Plugin):
            window = self._package.package.gui_tree
        else:
            window = GWindow(self._package.name, self._package)
        for tab_element in self._root.iterfind('tab'):
            tab = self._parse_tab(tab_element)
            tab.parent = window
            window.append(tab)
        self._package.gui_tree = window

    def _parse_tab(self, tab_element):
        name = tab_element.get('name')
        tab = GTab(name, self._package)
        # tab.icon = tab_element.findtext('tab_icon')
        for section_element in tab_element.iterfind('section'):
            section = self._parse_tab_section(section_element)
            section.parent = tab
            tab.append(section)
        return tab

    def _parse_tab_section(self, section_element):
        name = section_element.get('name')
        section = GSection(name, self._package)
        for entry_element in section_element.iterfind('import_entry'):
            name = entry_element.text
            if name:
                entry = self._package.tree.find_entry(name)
                section.append(entry)
        return section
