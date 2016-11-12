from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from lxml.etree import Element, ElementTree


__author__ = 'Ondřej Lanč'


class HelpFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        help_file = self._config.help_file
        log.info("Loading Help file {}".format(help_file))
        super().__init__(help_file)

    def parse(self):
        name=self._root.get('name')
        try:
            assert name == self._package.tree.name
        except AssertionError:
            log.error('invalid name of root element')
        containers=self._root.findall('container')
        for container in containers:
            self._parse_container(container, self._package.tree)
        entries=self._root.findall('entry')
        for entry in entries:
            self._parse_entry(entry, self._package.tree)

    def _parse_container(self, container_element, parent):
        name=container_element.get('name')
        this_container=parent.get_entry(name)
        self._set_help_label(this_container, container_element)
        containers=container_element.findall('container')
        for container in containers:
            self._parse_container(container, this_container)
        entries=container_element.findall('entry')
        for entry in entries:
            self._parse_entry(entry, this_container)

    def _parse_entry(self, entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        self._set_help_label(entry, entry_element)

    def _set_help_label(self, entry, entry_element):
        entry.label = entry_element.findtext('label')
        entry.help = entry_element.findtext('help')
