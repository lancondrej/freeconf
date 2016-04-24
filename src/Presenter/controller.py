from IO.Input.XMLPackageParser.parser import XMLParser
from Model.package import PackageBase
from os.path import expanduser
import configparser

__author__ = 'Ondřej Lanč'


class Controller(object):
    def __init__(self, name=""):
        self._freeconf_dirs = []
        self._package = None

    def load_config(self, file="config/freeconf.conf"):
        config = configparser.ConfigParser()
        config.read(file)
        self.freeconf_dirs(config["DEFAULT"]["locations"])

    @property
    def freeconf_dirs(self):
        return self._freeconf_dirs

    @freeconf_dirs.setter
    def freeconf_dirs(self, freeconf_dirs):
        for location in freeconf_dirs:
            self._freeconf_dirs.append(expanduser(location))

    def find_packages(self):
        pass

    def load_package(self, name=""):
        if name=="":
            self._load_test_package()
        else:
            pass

    def _load_test_package(self):
        input_parser = XMLParser("/home/ondra/škola/Freeconf/Freeconf/packages/test")
        self._package = PackageBase("test")
        input_parser.package=self._package
        self._package.current_language = "en"
        input_parser.load_package()
        input_parser.load_plugins()
        del input_parser

    def tabs(self):
        return [(tab.name, tab.label) for tab in self._package.gui_tree._entries]

    def tab(self, name):
        return self._package.gui_tree.get_entry(name).content._entries
