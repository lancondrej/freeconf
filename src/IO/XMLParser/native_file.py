import lxml.etree as ET

from src.IO.XMLParser.config_file import ConfigFileWriter

__author__ = 'Ondřej Lanč'


class NativeFileWriter (object):
    def __init__(self, group, dom):
        self._group = group
        self._dom = dom

    def write_native(self):
        xslt = ET.parse(self._group.transform_file)
        transform = ET.XSLT(xslt)
        newdom = transform(self._dom)
        f = open(self._group.native_output, 'w')
        f.write(str(newdom))