from src.Model.Config.freeconf_config import Config
import xml.etree.ElementTree as ET
from os import scandir

from src.Model.Config.package import Package

__author__ = 'Ondřej Lanč'


class ConfigPresenter(object):
    def __init__(self):
        self._config = Config()
        self._load_config()

    @property
    def packages_list(self):
        return list(self._config.packages.keys())

    def package(self, name):
        return self._config.package(name)

    def _load_config(self):
        tree = ET.parse(self._config.config_file)
        root = tree.getroot()
        for package in root.findall('packages_dir'):
            self._load_packages(package.find('location').text)
        for lang in root.findall('.general/lang'):
                self._config.lang.append(lang.text)

    def _load_packages(self, dir):
        for package in scandir(dir):
            p = self._load_package_info(package)
            self._config.packages[p.name] = p

    def _load_package_info(self, dir):
        package = Package()
        package.location=dir.path
        package.name=dir.name
        self._load_avaiable_plugins(package)
        self._load_avaiable_languages(package)
        return package

    def _load_avaiable_plugins(self, package):
        try:
            for plugin in scandir(package.plugins_dir):
                package.available_plugins.append(plugin.name)
        except FileNotFoundError:
            pass
        # TODO: zpráva do logu

    def _load_avaiable_languages(self, package):
        try:
            for lang in scandir(package.languages_dir):
                package.available_language.append(lang.name)
        except FileNotFoundError:
            pass
        # TODO: zpráva do logu