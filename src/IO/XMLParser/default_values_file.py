from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log


__author__ = 'Ondřej Lanč'


class DefaultValuesFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        list_file = self._config.default_values_file
        log.info("Loading default values file {}".format(list_file))
        super().__init__(list_file)

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
        parent=parent.get_entry(name)
        if parent.is_multiple_entry_container():
            parent = parent.append_default()
        containers=container_element.findall('container')
        for container in containers:
            self._parse_container(container, parent)
        entries=container_element.findall('entry')
        for entry in entries:
            self._parse_entry(entry, parent)

    def _parse_entry(self, entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        value = entry_element.findtext('value')
        if entry.is_multiple_entry_container():
            entry = entry.append_default()
        entry.default_value = value




