#!/usr/bin/python3
# -*- coding: utf-8 -*-#

import os

__author__ = 'Ondřej Lanč'


class Package(object):
    """Store information about one single package. """
    def __init__(self):
        self.name = ""
        self.location = ""
        self.file = self.Files()
        self._groups = {}
        self.available_language = []
        self.author = None
        self.default_language = None
        self._plugins = {}
        self.root = self

    @property
    def header_file(self):
        """header file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.header) if self.file.header else None

    @property
    def list_file(self):
        """list file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.list) if self.file.list else None

    @property
    def template_file(self):
        """template file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.template) if self.file.template else None

    @property
    def dependencies_file(self):
        """dependencies file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.dependencies) if self.file.dependencies else None

    @property
    def gui_template_file(self):
        """gui template file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.gui_template) if self.file.gui_template else None

    def help_file(self, language):
        """help file location
        :param language: language code ('en', 'cs' ...)
        :return full path of file or None if file not set
        """
        language = self._set_language(language)
        return os.path.join(self.languages_dir, language, self.file.help) if self.file.help else None

    def list_help_file(self, language):
        """list help file location
        :param language: language code ('en', 'cs' ...)
        :return full path of file or None if file not set
        """
        language = self._set_language(language)
        return os.path.join(self.languages_dir, language, self.file.list) if (self.file.list and language) else None

    def gui_help_file(self, language):
        """gui help file location
        :param language: language code ('en', 'cs' ...)
        :return full path of file or None if file not set
        """
        language = self._set_language(language)
        return os.path.join(self.languages_dir, language, self.file.gui_label) if (self.file.gui_label and language) else None

    @property
    def default_values_file(self):
        """default values file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.default_values) if self.file.default_values else None

    @property
    def config_file(self):
        """output config file location
        :return full path of file or None if file not set
        """
        return os.path.join(self.location, self.file.output) if self.file.output else None

    @property
    def plugins_dir(self):
        """plugins dir location
        :return full path of dir
        """
        return os.path.join(self.location, 'plugins')

    @property
    def languages_dir(self):
        """language dir location
        :return full path of dir
        """
        return os.path.join(self.location, 'L10n')

    @property
    def groups(self):
        """ groups getter
        :return dict: groups dictionary
        """
        return self._groups

    def group(self, name='default'):
        """ group getter
        :param name: name of group
        :return Group: Group used in Package
        """
        return self._groups.get(name)

    def add_group(self, group):
        """ add group to package. Set self as group package.
        :param group
        """
        group.package=self
        self._groups[group.name] = group

    def add_plugin(self, plugin):
        """ add plugin config to package config. Set self as plugin parent.
        :param plugin
        """
        plugin.parent=self
        plugin.root=self.root
        self._plugins[plugin.name]=plugin

    @property
    def plugins(self):
        """ plugins getter
        :return dict: plugin dictionary
        """
        return self._plugins

    def plugin(self, name):
        """ plugin getter
        :param name: name of plugin
        :return Plugin: Plugin in Package
        """
        return self._plugins.get(name)

    def _set_language(self, lang):
        """set lang if lang is not in available retrun default
        :param lang: code of language
        :return code of language"""

        if lang not in self.available_language:
            lang = self.default_language
        if lang not in self.available_language:
            lang = None
        if lang is None:
            lang = self.available_language[0]
        return lang

    class Files(object):
        """Store names of files in configuration package"""
        def __init__(self):
            self.header = "header.xml"
            self.list = None
            self.template = None
            self.dependencies = None
            self.gui_template = None
            self.help = None
            self.gui_label = None
            self.default_values = None
            self.output = None


class Plugin(Package):
    """Store information about one plugin of package. """

    def __init__(self):
        Package.__init__(self)
        self.parent = None