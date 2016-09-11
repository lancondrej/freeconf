import xml.etree.ElementTree as ET


__author__ = 'Ondřej Lanč'

class Config(object):
    def __init__(self):
        self._config_file = "freeconf.xml"
        self._packages={}
        self._lang = []
        self._load_config()

    def _load_config(self):
        tree = ET.parse(self._config_file)
        root = tree.getroot()