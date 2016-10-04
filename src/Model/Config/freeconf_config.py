import xml.etree.ElementTree as ET

from src.Model.Config.package import Package

__author__ = 'Ondřej Lanč'

class Config(object):
    def __init__(self):
        self._config_file = "freeconf.conf"
        self._packages={}
        self._lang = []
        self._load_config()

    def _load_config(self):
        tree = ET.parse(self._config_file)
        root = tree.getroot()
        for package in root.findall('package'):
            p = Package()
            p.name = package.find('name').text
            p.location = package.find('location').text
            p.output = package.find('output').text
            p.native = package.find('native').text
            p.xslt = package.find('xslt').text
            self._packages[p.name]=p
        for lang in root.findall('.general/lang'):
                self._lang.append(lang.text)

    @property
    def packages(self):
        return self._packages.keys()

    def package(self, name):
        return self._packages[name]