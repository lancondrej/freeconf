#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.IO.XMLParser.file_reader import FileReader
from src.IO.log import logger
from src.Model.Package.entries.multiple.multiple_entry import MultipleEntry

__author__ = 'Ondřej Lanč'


class DefaultValuesFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        default_values_file = self._config.default_values_file
        logger.info("Loading default values file {}".format(default_values_file))
        super().__init__(default_values_file)

    def parse(self):
        for container in self._root.iterfind('container'):
            self._parse_container(container, self._package.tree)
        for entry in self._root.iterfind('entry'):
            self._parse_entry(entry, self._package.tree)

    def _parse_container(self, container_element, parent):
        name=container_element.get('name')
        this_container=parent.get_entry(name)
        if isinstance(this_container, MultipleEntry):
            this_container = this_container.append_default()
        for container in container_element.iterfind('container'):
            self._parse_container(container, this_container)
        for entry in container_element.iterfind('entry'):
            self._parse_entry(entry, this_container)

    def _parse_entry(self, entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        if entry is not None:
            value = entry_element.text
            if isinstance(entry, MultipleEntry):
                entry = entry.append_default()
            entry.default_value = value




