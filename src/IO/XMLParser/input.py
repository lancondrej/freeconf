#!/usr/bin/python3
#
import os

from src.IO.XMLParser.config_file import ConfigFileReader
from src.IO.XMLParser.default_values_file import DefaultValuesFileReader
from src.IO.XMLParser.gui_help_file import GUIHelpFileReader
from src.IO.XMLParser.gui_template_file import GUITemplateFileReader
from src.IO.XMLParser.help_file import HelpFileReader
from src.IO.XMLParser.list_help_file import ListHelpFileReader
from src.Model.Package.package import Package, Plugin
from src.IO.XMLParser.header_file import HeaderFileReader
from src.IO.XMLParser.list_file import ListFileReader
from src.IO.XMLParser.template_file import TemplateFileReader
from src.IO.input import Input
from src.IO.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class XMLParser(Input):
    def __init__(self, config, package):
        # configuration of package
        self._config = config
        # package itself
        self._package = package

    def load_package(self):
        self._load_header()
        self._load_lists()
        self._load_template()
        self._load_GUI_template()
        self._load_help('en')
        self._load_list_help('en')
        self._load_GUI_help('en')
        self._load_default_value()
        self._load_config()
        return self._package

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

    def load_plugin(self, plugins=None):
        if plugins:
            for plugin in plugins:
                if plugin in self._config.avaiable_plugins:
                    self._load_plugin(plugin)
        else:
            for plugin in self._config.avaiable_plugins:
                self._load_plugin(plugin)

    def _load_plugin(self, plugin_name):
        plugin = Plugin(plugin_name, self._package)
        input_parser=XMLParser(self._config.plugin(plugin_name), plugin)
        input_parser.load_package()
        self._package.plugins.append(plugin)

    def load_config(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    def load_packages_config(self):
        pass