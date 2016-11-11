import xml.etree.ElementTree as ET

__author__ = 'Ondřej Lanč'


class FileReader(object):

    def __init__(self, file):
        self._file=file
        self._root = self._get_root()

    def _get_root(self):
        return ET.parse(self._file).getroot()

    def parse(self):
        raise NotImplementedError