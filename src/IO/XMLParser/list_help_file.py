#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.IO.XMLParser.file import FileReader


__author__ = 'Ondřej Lanč'


class ListHelpFileReader(FileReader):
    def __init__(self, config, package, language):
        self._config = config
        self._package = package
        list_help_file = self._config.list_help_file(language)
        super().__init__(list_help_file)
        self.logger.info("Loading List help file {}".format(list_help_file))

    def parse(self):
        for list_element in self._root.iterfind('list'):
            self.logger.info("List file: parsing <list> element")
            name = list_element.get('name')
            if name:
                try:
                    list=self._package.lists[name]
                    self._parse_entry(list, list_element)
                except KeyError:
                    self.logger.error("No list {} in package".format(name))
            else:
                self.logger.error("List file: in element <list> missing attribute name")

    def _parse_entry(self, list, list_element):
        for entry in list_element.iterfind('entry'):
            value = entry.get('value')
            if value:
                list_entry = list.get_entry(value)
                if list_entry is not None:
                    list_entry.label = entry.findtext('label')
                    list_entry.help = entry.findtext('help')
            else:
                self.logger.error("list entry name not defined")
