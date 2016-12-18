#!/usr/bin/python3
# -*- coding: utf-8 -*-
from src.Model.Config.freeconf_config import Config
import xml.etree.ElementTree as ET
from os import scandir

from src.Model.Config.package import Package, Plugin
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class ConfigPresenter(Presenter):
    """presenter for manipulating with config object"""
    def __init__(self):
        super().__init__()
        self._config = Config()
        self._load_config()

    @property
    def packages_list(self):
        """

        :return: list of available packages configuration
        """
        return list(self._config.packages.keys())

    def package(self, name):
        """

        :param name: name of package
        :return: return configuration of package or None
        """
        return self._config.package(name)

    def reload_config(self):
        """roload freeconf configurations

        """
        self._config = Config()
        self._load_config()

    def _load_config(self):
        """load freecof configuration from freeconf.xml

        :return:
        """
        tree = ET.parse(self._config.config_file)
        root = tree.getroot()
        for package in root.findall('packages_dir'):
            self._load_packages(package.find('location').text)
        self._config.lang = root.findtext('.general/lang')

    def _load_packages(self, dir):
        """find available packages in packages directory

        :param dir: directory for scan
        """
        for package in scandir(dir):
            p = self._load_package_info(package)
            self._config.packages[p.name] = p

    def _load_package_info(self, dir, class_name=Package):
        """load info about package

        :param dir: packages directory
        :param class_name: Package or Plugin
        :return: configuration of package object
        """
        package = class_name()
        package.location = dir.path
        package.name = dir.name
        self._load_avaiable_plugins(package)
        self._load_available_languages(package)
        return package

    def _load_avaiable_plugins(self, package):
        """find available plugins in plugins directory

        :param package: base package
        """
        try:
            for plugin_dir in scandir(package.plugins_dir):
                package.add_plugin(self._load_package_info(plugin_dir, Plugin))
        except FileNotFoundError:
            pass
            # TODO: zpráva do logu

    def _load_available_languages(self, package):
        """find available languages for given package

        :param package: config package object
        """
        try:
            for lang in scandir(package.languages_dir):
                package.available_languages.append(lang.name)
        except FileNotFoundError:
            pass
            # TODO: zpráva do logu

    @property
    def language(self):
        """language getter

        :return: lang code
        """
        return self._config.lang
