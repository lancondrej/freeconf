import os
from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Package.entries.bool import Bool
from src.Model.Package.entries.container import Container
from src.Model.Package.entries.fuzzy import Fuzzy
from src.Model.Package.entries.multiple.multiple_container import MultipleContainer
from src.Model.Package.entries.multiple.multiple_key_word import MultipleKeyWord
from src.Model.Package.entries.number import Number
from src.Model.Package.entries.string import String
from src.Model.Package.package import Plugin

__author__ = 'Ondřej Lanč'


class EntryType(object):
    def __init__(self, name, name_element, class_name, multiple,function=None):
        self.name = name
        self.name_element = name_element
        self.class_name = class_name
        self.multiple_class = multiple
        self.inside_func = function


class TemplateFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        template_file = self._config.template_file
        log.info("Loading template file {}".format(template_file))
        super().__init__(template_file)

    def parse(self):
        name = self._root.findtext('container-name')
        if name:
            if isinstance(self._package, Plugin):
                container = self._package.package.tree
                if container.name != name:
                    raise ParseError("Plugin root container is different from Package root Container")
            else:
                container = Container(name)
                container.group = self._config.group()
            for entry in self._parse_entry(self._root):
                container.add_entry(entry)
                # add default group
            self._package.tree = container
        else:
            raise ParseError('root container name missing')

    def _parse_entry(self, container_element):
        for element_type in self.types:
            for entry in self._parse_entry_of_type(container_element, element_type):
                yield entry

    def _parse_entry_of_type(self, container_element, element_type):
        elements=container_element.findall(element_type.name)
        for element in elements:
            name = element.findtext(element_type.name_element)
            if name:
                entry = element_type.class_name(name)
                # Multiple manipulation
                multiple = element.find('multiple')
                if multiple:
                    entry = element_type.multiple_class(entry)
                    value = multiple.findtext('max')
                    if value is not None:
                        entry.multiple_max = int(value)
                    value = multiple.findtext('min')
                    if value is not None:
                        entry.multiple_min = int(value)
                    entry.primary = multiple.findtext('primary')
                # BaseEntry properties
                # active
                value = element.findtext('active')
                if value is not None:
                    entry.static_active = True if value == 'yes' else False
                # mandatory
                value = element.findtext('mandatory')
                if value is not None:
                    entry.static_mandatory = True if value == 'yes' else False
                # group
                value = element.findtext('group')
                if value is not None:
                    entry.group=self._config.group(value)
                # other properties for specific type, and container recursion
                if element_type.inside_func:
                    element_type.inside_func(self, entry, element)
                yield entry
            else:
                raise ParseError('{} name misssing'.format(element_type.name))



    def _inside_container(self, container, element):
        for entry in self._parse_entry(element):
            container.add_entry(entry)

    def _inside_number(self, entry, element):
        properties = element.find('properties')
        if properties:
            value=properties.findtext('max')
            if value is not None:
                entry.max = float(value)
            value=properties.findtext('min')
            if value is not None:
                entry.min = float(value)
            value=properties.findtext('step')
            if value is not None:
                entry.step = float(value)
            value=properties.findtext('precision')
            if value is not None:
                entry.precision = float(value)
            value=properties.findtext('print-sign')
            if value is not None:
                entry.print_sign = True if value == 'yes' else False
            value=properties.findtext('leading-zeros')
            if value is not None:
                entry.leading_zeros = True if value == 'yes' else False

    def _inside_string(self, entry, element):
        properties = element.find('properties')
        if properties:
            value=properties.findtext('regexp')
            if value is not None:
                entry.reg_exp=value
            value = properties.findtext('data')
            if value is not None:
                list=self._package.lists.get(value)
                entry.list=list

    def _inside_fuzzy(self, entry, element):
        properties = element.find('properties')
        if properties:
            value = properties.findtext('data')
            if value is not None:
                list = self._package.lists.get(value)
                entry.list = list

    types = [
        EntryType('container', 'container-name', Container, MultipleContainer, _inside_container),
        EntryType('bool', 'entry-name', Bool, MultipleKeyWord),
        EntryType('string', 'entry-name', String, MultipleKeyWord, _inside_string),
        EntryType('fuzzy', 'entry-name', Fuzzy, MultipleKeyWord, _inside_fuzzy),
        EntryType('number', 'entry-name', Number, MultipleKeyWord, _inside_number)
    ]

