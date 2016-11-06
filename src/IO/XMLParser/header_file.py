import xml.etree.ElementTree as ET
from src.IO.XMLParser.file_reader import FileReader
from src.Model.Config.package import Package

__author__ = 'Ondřej Lanč'


class HeaderFileReader(FileReader):
    def __init__(self, file):
        self._file=file
        self._root=self._get_root()
        self._package=Package()

    def _get_root(self):
        return ET.parse(self._file).getroot()

    def read(self):
        self.load_group()
        self.load_package()
        return self._package

    def content(self):
        pass

    def load_package(self):
        package_element = self._root.find('package')
        self._package.name = package_element.find('name').text
        self._package.default_language = package_element.find('default-language').text
        # package.location = package_element.find('location').text
        # package.output = package_element.find('output').text
        # package.native = package_element.find('native').text
        # package.xslt = package_element.find('xslt').text

    def load_group(self):
        for group in self._root.findall('entry-group'):
            name = group.get('name')
            group.find('transform')
            group.find('native-output')
            group.find('output-defaults')

    def find_language(self):
        pass