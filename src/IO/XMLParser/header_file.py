import xml.etree.ElementTree as ET
from src.IO.XMLParser.file_reader import FileReader

__author__ = 'Ondřej Lanč'


class HeaderFileReader(FileReader):
    def __init__(self, file):
        self.file=file

    def read(self):

        root = ET.parse(self.file).getroot()

        for group in root.findall('entry-group'):
            name = group.get('name')
            group.find('transform')
            group.find('native-output')
            group.find('output-defaults')

        for package in root.findall('package'):
            p = PackageConfig()
            p.name = package.find('name').text
            p.location = package.find('location').text
            p.output = package.find('output').text
            p.native = package.find('native').text
            p.xslt = package.find('xslt').text
            self._packages[p.name] = p

        for lang in root.findall('.general/lang'):
            self._lang.append(lang.text)
