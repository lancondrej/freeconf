from lxml.etree import Element, ElementTree

from src.IO.XMLParser.file_reader import FileReader
from src.IO.log import logger
from src.Model.Package.entries.multiple.multiple_entry import MultipleEntry

__author__ = 'Ondřej Lanč'


class ConfigFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        config_file = self._config.config_file
        logger.info("Loading List file {}".format(config_file))
        super().__init__(config_file)

    def parse(self):

        root_container=self._root.find('container')
        name = root_container.get('name')
        try:
            assert name == self._package.tree.name
        except AssertionError:
            logger.error('invalid name of root element')
        containers = root_container.iterfind('container')
        for container in containers:
            self._parse_container(container, self._package.tree)
        entries = root_container.iterfind('entry')
        for entry in entries:
            self._parse_entry(entry, self._package.tree)

    def _parse_container(self, container_element, parent):
        name = container_element.get('name')
        this_container = parent.get_entry(name)
        if isinstance(this_container, MultipleEntry):
            this_container = this_container.append()
        containers = container_element.iterfind('container')
        for container in containers:
            self._parse_container(container, this_container)
        entries = container_element.iterfind('entry')
        for entry in entries:
            self._parse_entry(entry, this_container)

    @staticmethod
    def _parse_entry(entry_element, parent):
        name = entry_element.get('name')
        entry = parent.get_entry(name)
        value = entry_element.findtext('value')
        if isinstance(entry, MultipleEntry):
            entry = entry.append()
        entry.value = value


class ConfigFileWriter(object):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        self.render = {
            'Container': self.render_container,
            'Fuzzy': self.render_key_word,
            'Bool': self.render_key_word,
            'Number': self.render_key_word,
            'String': self.render_key_word,
            'MultipleContainer': self.render_multiple,
            'MultipleKeyWord': self.render_multiple,
        }
        self._root = package.tree

    def write_config(self, file=None):
        config_tree = self.get_config()
        config_tree.write(file or self._config.config_file, encoding="UTF-8", xml_declaration=True, pretty_print=True)

    def get_config(self, group=None):
        root = Element('freeconf_config')
        root_container = self.render_container(self._root, group)[0]
        root.append(root_container)
        return ElementTree(root)

    def render_entry(self, entry, group):
        try:
            return self.render[type(entry).__name__](entry, group)
        except:
            pass

    def render_container(self, container, group):
        element = Element('container')
        element.set('name', container.name)
        for entry in container.entries.values():
            sub_element = self.render_entry(entry, group)
            if sub_element:
                element.extend(sub_element)
        if len(element):
            return [element]
        return

    def render_key_word(self, entry, group):
        if group:
            if entry.group != group:
                return
        if entry.package != self._package:
            return
        element = Element('entry')
        element.set('name', entry.name)
        value = entry.value
        if value is None:
            logger.info("Value for entry {} missing".format(entry.full_name))
            return
        val_el = Element('value')
        val_el.text = str(value)
        element.append(val_el)

        # if group:
        #     help_text = entry.help
        #     if help_text:
        #         help_el = Element('help')
        #         help_el.text = help_text
        #         element.append(help_el)

        return [element]

    def render_multiple(self, mult, group):
        rendered = [self.render_entry(entry, group) for entry in mult.entries]
        if rendered:
            return rendered[0]
        return
