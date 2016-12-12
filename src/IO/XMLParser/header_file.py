#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os
import re

from src.IO.XMLParser.file import FileReader
from src.IO.exception import *
from src.Model.Config.group import Group, default
from src.Model.Config.package import Plugin

__author__ = 'Ondřej Lanč'


class HeaderFileReader(FileReader):
    def __init__(self, config):
        self._config = config
        header_file = self._config.header_file
        super().__init__(header_file)
        self.logger.info("Loading header file {}".format(header_file))

    def parse(self):
        self.parse_package_info()
        self.parse_content()
        self.parse_group()

    def parse_content(self):
        content_element = self._root.find('content')
        if content_element:
            self.logger.debug("Header file: parsing <content> element")

            file = content_element.findtext('template')
            if file is None:
                raise MissingMandatoryElementError("<template> in  header file")
            self.logger.debug("Header file: template file {}".format(file))
            self._config.file.template = file

            file = content_element.findtext('output')
            if file is None:
                raise MissingMandatoryElementError("<output> in  header file")
            self.logger.debug("Header file: output file {}".format(file))
            self._config.file.output = file

            file = content_element.findtext('default_values')
            if file is not None:
                self.logger.debug("Header file: default value file {}".format(file))
                self._config.file.default_values = file

            file = content_element.findtext('help')
            if file is not None:
                self.logger.debug("Header file: help file {}".format(file))
                self._config.file.help = file

            # file = content_element.findtext('dependencies')
            # self._config.file.dependencies = file

            file = content_element.findtext('gui_template')
            if file is not None:
                self.logger.debug("Header file: gui template file {}".format(file))
                self._config.file.gui_template = file

            file = content_element.findtext('gui_label')
            if file is not None:
                self.logger.debug("Header file: gui label file {}".format(file))
                self._config.file.gui_label = file

            file = content_element.findtext('lists')
            if file is not None:
                self.logger.debug("Header file: list file {}".format(file))
                self._config.file.list = file
        else:
            raise MissingMandatoryElementError("<content> in  header file")

    def parse_group(self):
        group_not_set = True

        for group_element in self._root.iterfind('entry_group'):
            self.logger.debug("Header file: parsing <entry_group> element")
            name = group_element.get('name')
            if name is not None and name != 'default':
                group = Group(name)
            else:
                group = default
                # TODO: omezit na jedno použití abych nepřepisoval
            group.transform_file = group_element.findtext('transform')
            group._native_output = self._expand_file_name(group_element.findtext('native_output'))
            group.output_defaults = True if group_element.findtext('output_defaults') == 'yes' else False
            self._config.add_group(group)
            group_not_set = False

        if isinstance(self._config, Plugin):
            for group_element in self._root.iterfind('change_group'):
                self.logger.info("Header file: parsing <change_group> element")
                name = group_element.get('name')
                group=self._config.parent.group(name)
                if group:
                    group.include_transform(self._config, group_element.findtext('add_transform'))
                else:
                    self.logger.error("group name {} is not in Package".format(name))

    def parse_package_info(self):
        self._config.author = self._root.findtext('author')
        self._config.default_language = self._root.findtext('default_language')

    def _expand_file_name(self, file):
        # TODO: vyřešit kdy to používat a kdy ne + jestl ito nemá být raději u package/group (problém s list a jazyky)
        def _home_dir():
            """Get HOME location."""
            try:
                return os.environ['HOME']
            except KeyError:
                self.logger.warning('Unable to get the location of HOME directory!')
                return None

        def _package_dir():
            return self._config.root.location

        def _parent_dir():
            if isinstance(self._config, Plugin):
                return self._config.parent.location
            else:
                self.logger.warning('Using of $PARENT variable in base Package. Ignoring variable.')
                return None

        def _plugin_dir():
            if isinstance(self._config, Plugin):
                return self._config.location
            else:
                self.logger.warning('Using of $PLUGIN variable in base Package. Ignoring variable.')

        def _this_dir():
            return self._config.location

        variables={
            "HOME": _home_dir,
            "PACKAGE": _package_dir,
            "PLUGIN": _plugin_dir,
            "PARENT": _parent_dir,
        }

        # TODO: vyřešit strukturu sub pluginů samozřejmě i v config a package
        val = None
        match = re.match(r"\$\{?(?P<env>\w+)\}?/(?P<file>.+)", file)
        if match:
            var = match.group('env')
            file = match.group('file')
            if var in variables:
                val = variables[var]()
            else:
                val = None
                self.logger.warning("Variable {} not found in allowed list".format(var))
        if val is None:
            # If variable is not found, replace it's occurence with empty string
            val = _this_dir()
            match = re.match(r"/", file)
            if match:
                val = ""
        file = os.path.normpath(os.path.join(val, file))
        return file



