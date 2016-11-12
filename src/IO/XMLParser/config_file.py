from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from lxml.etree import Element, ElementTree


__author__ = 'Ondřej Lanč'


class ConfigFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        config_file = self._config.config_file
        log.info("Loading List file {}".format(config_file))
        super().__init__(config_file)

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
        if this_container.is_multiple_entry_container():
            this_container = this_container.append()
        containers=container_element.findall('container')
        for container in containers:
            self._parse_container(container, this_container)
        entries=container_element.findall('entry')
        for entry in entries:
            self._parse_entry(entry, this_container)

    def _parse_entry(self, entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        value = entry_element.findtext('value')
        if entry.is_multiple_entry_container():
            entry = entry.append()
        entry.value = value


class ConfigFileWriter (object):
    def __init__(self, root):
        self.render = {
            'Container': self.render_container,
            'Fuzzy': self.render_key_word,
            'Bool': self.render_key_word,
            'Number': self.render_key_word,
            'String': self.render_key_word,
            'MultipleContainer': self.render_multiple,
            'MultipleKeyWord': self.render_multiple,
        }
        self._root = root

    def write_config(self, file):
        config_tree = self.get_config()
        config_tree.write(file, encoding="UTF-8", xml_declaration=True, pretty_print=True)

    def get_config(self):
        root = self.render_entry(self._root)[0]
        return ElementTree(root)

    def render_entry(self, entry):
        try:
            return self.render[type(entry).__name__](entry)
        except:
            pass

    def render_container(self, container):
        element = Element('container')
        element.set('name', container.name)
        for entry in container.entries.values():
            sub=self.render_entry(entry)
            element.extend(self.render_entry(entry))
        return [element]

    def render_key_word(self, entry):
        element = Element('entry')
        element.set('name', entry.name)
        # element.set('group', entry.group.name)
        value=Element('value')
        value.text = str(entry.value)
        element.append(value)
        return [element]

    def render_multiple(self, mult):
        return [self.render_entry(entry)[0] for entry in mult.entries]


