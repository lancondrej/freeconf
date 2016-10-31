import xml.etree.ElementTree as ET
from os import scandir

from src.Model.Config.package_config import PackageConfig

__author__ = 'Ondřej Lanč'

class Config(object):
    def __init__(self):
        self._config_file = "freeconf.xml"
        self._packages_dir=[]
        self._packages={}
        self._lang = []
        self._load_config()

        self.homeDir = ""
        self.packageDir = ""
        self.helpDirs = {}
        self.listDir = ""
        self.defaultValuesDir = ""
        self.listFiles = {}


        # self.templateFile = FcFileLocation()
        # self.dependenciesFile = FcFileLocation()
        # self.guiTemplateFile = FcFileLocation()
        # self.helpFile = FcFileLocation()
        # self.guiLabelFile = FcFileLocation()
        # self.defaultValuesFile = FcFileLocation()
        # self.outputFile = FcFileLocation()
        #

    def _load_config(self):
        tree = ET.parse(self._config_file)
        root = tree.getroot()
        for package in root.findall('packages_dir'):
            self._packages_dir.append(package.find('location').text)
        for lang in root.findall('.general/lang'):
                self._lang.append(lang.text)
        self._find_packages()

    def _find_packages(self):
        for dir in self._packages_dir:
            for package in scandir(dir):
                print(package.path)

    @property
    def packages(self):
        return self._packages.keys()

    def package(self, name):
        return self._packages[name]