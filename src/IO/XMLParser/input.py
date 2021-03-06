#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.IO.XMLParser.config_file import ConfigFileReader
from src.IO.XMLParser.default_values_file import DefaultValuesFileReader
from src.IO.XMLParser.gui_help_file import GUIHelpFileReader
from src.IO.XMLParser.gui_template_file import GUITemplateFileReader
from src.IO.XMLParser.header_file import HeaderFileReader
from src.IO.XMLParser.help_file import HelpFileReader
from src.IO.XMLParser.list_file import ListFileReader
from src.IO.XMLParser.list_help_file import ListHelpFileReader
from src.IO.XMLParser.template_file import TemplateFileReader
from src.IO.input import Input
from src.Model.Package.package import Plugin

__author__ = 'Ondřej Lanč'


class XMLParser(Input):
    def __init__(self, config, package):
        # configuration of package
        self._config = config
        # package itself
        self._package = package
        self.logger = logging.getLogger('IO')

    def load_package(self, lang=None):
        self._load_header()
        try:
            self._load_lists()
            try:
                self._load_list_help(lang)
            except FileExistsError:
                self.logger.debug("list help file missing")
        except FileExistsError:
            self.logger.debug("list file missing")
        self._load_template()
        try:
            self._load_help(lang)
        except FileExistsError:
            self.logger.debug("help file missing")
        try:
            self._load_GUI_template()
            try:
                self._load_GUI_help(lang)
            except FileExistsError:
                self.logger.debug("gui help file missing")
        except FileExistsError:
            self.logger.debug("gui template file missing")

        try:
            self._load_default_value()
        except FileExistsError:
            self.logger.debug("default_value file missing")
        try:
            self._load_config()
        except FileExistsError:
            self.logger.debug("config file missing")
            self._set_default_value()

        return self._package

    def _set_default_value(self):
        self._package.tree.set_default()

    def _load_header(self):
        """Load header file. Support function for load_package."""
        HeaderFileReader(self._config).parse()

    def _load_lists(self, ):
        """Load list files."""
        ListFileReader(self._config, self._package).parse()

    def _load_template(self):
        """Load template file. Support function for load_package."""
        TemplateFileReader(self._config, self._package).parse()

    def _load_default_value(self):
        """Load file with default values"""
        DefaultValuesFileReader(self._config, self._package).parse()

    def _load_config(self):
        """Load config file ignore help, only load like default values"""
        ConfigFileReader(self._config, self._package).parse()

    def _load_help(self, language=None):
        """Load help file"""
        HelpFileReader(self._config, self._package, language).parse()

    def _load_list_help(self, language=None):
        """Load list help file"""
        ListHelpFileReader(self._config, self._package, language).parse()

    def _load_GUI_template(self):
        GUITemplateFileReader(self._config, self._package).parse()

    def _load_GUI_help(self, language=None):
        GUIHelpFileReader(self._config, self._package, language).parse()

    def load_plugin(self, lang=None, plugins=None):
        if plugins:
            for plugin in plugins:
                if plugin in self._config.plugins:
                    self._load_plugin(plugin, lang)
        else:
            for plugin in self._config.plugins:
                self._load_plugin(plugin, lang)

    def _load_plugin(self, plugin_name, lang):
        plugin = Plugin(plugin_name, self._package)
        input_parser = XMLParser(self._config.plugin(plugin_name), plugin)
        input_parser.load_package(lang)
        self._package.plugins.append(plugin)

    def load_config(self, source):
        self._load_config()
