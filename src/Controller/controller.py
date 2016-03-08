from os.path import expanduser
import configparser

__author__ = 'Ondřej Lanč'


class Controller(object):
    def __init__(self, name=""):
        self._freeconf_dirs = []

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