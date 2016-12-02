from src.IO.XMLParser.file_reader import FileReader
from src.IO.log import logger


__author__ = 'Ondřej Lanč'


class HelpFileReader(FileReader):
    def __init__(self, config, package, language):
        self._config = config
        self._package = package
        help_file = self._config.help_file(language)
        logger.info("Loading Help file {}".format(help_file))
        super().__init__(help_file)

    def parse(self):
        root_container=self._root.find('container')
        if root_container:
            name=root_container.get('name')
            try:
                assert name == self._package.tree.name
            except AssertionError:
                logger.error('invalid name of root element')
            for container in root_container.iterfind('container'):
                self._parse_container(container, self._package.tree)
            for entry in root_container.iterfind('entry'):
                self._parse_entry(entry, self._package.tree)

    def _parse_container(self, container_element, parent):
        name=container_element.get('name')
        this_container=parent.get_entry(name)
        if this_container:
            self._set_help_label(this_container, container_element)
            for container in container_element.iterfind('container'):
                self._parse_container(container, this_container)
            for entry in container_element.iterfind('entry'):
                self._parse_entry(entry, this_container)

    def _parse_entry(self, entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        self._set_help_label(entry, entry_element)

    def _set_help_label(self, entry, entry_element):
        if entry is not None:
            entry.label = entry_element.findtext('label')
            entry.help = entry_element.findtext('help')
