#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.IO.XMLParser.file import FileReader

__author__ = 'Ondřej Lanč'


class GUIHelpFileReader(FileReader):
    def __init__(self, config, package, language):
        self._config = config
        self._package = package
        gui_help_file = self._config.gui_help_file(language)
        super().__init__(gui_help_file)
        self.logger.info("Loading GUI help file {}".format(gui_help_file))

    def parse(self):
        label = self._root.findtext('label')
        if label:
            self._package.gui_tree.label = label
        description = self._root.findtext('description')
        if description:
            self._package.gui_tree.description = description
        for tab_element in self._root.iterfind('tab'):
            self._parse_tab(tab_element)

    def _parse_tab(self, tab_element):
        name = tab_element.get('name')
        tab = self._package.gui_tree.get_tab(name)
        tab.label = tab_element.findtext('label')
        tab.description = tab_element.findtext('description')
        for section_element in tab_element.iterfind('section'):
            self._parse_section(section_element, tab)

    def _parse_section(self, section_element, tab):
        name = section_element.get('name')
        section = tab.get_section(name)
        section.label = section_element.findtext('label')
        section.description = section_element.findtext('description')
