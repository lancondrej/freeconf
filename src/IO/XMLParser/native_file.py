import lxml.etree as ET

from src.IO.XMLParser.config_file import ConfigFileWriter

__author__ = 'Ondřej Lanč'


class NativeFileWriter (object):
    def __init__(self, native, xslt, config_file_writer):
        self._file = native
        self._xslt = xslt
        self._config_file_writer = config_file_writer

    def write_native(self):
        dom = self._config_file_writer.get_config()
        xslt = ET.parse(self._xslt)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        f = open(self._file, 'w')
        f.write(str(newdom))