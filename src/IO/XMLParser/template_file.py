import os
from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Config.group import Group
from src.Model.Package.entries.bool import Bool
from src.Model.Package.entries.container import Container
from src.Model.Package.entries.fuzzy import Fuzzy
from src.Model.Package.entries.number import Number
from src.Model.Package.entries.string import String

__author__ = 'Ondřej Lanč'


class EntryType(object):
    def __init__(self, name, name_element, class_name, function=None):
        self.name = name
        self.name_element = name_element
        self.class_name = class_name
        self.inside_func = function


class TemplateFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        template_file = self._config.template_file
        log.info("Loading template file {}".format(template_file))
        super().__init__(template_file)

    def parse(self):
        self._package.tree = self._parse_container(self._root)

    def _parse_container(self, container_element):
        name = container_element.findtext('container-name')
        if name:
            container = Container(name)
            for entry in self._parse_entry(container_element):
                container.add_entry(entry)
            return container
        else:
            raise ParseError('container name missing')

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
                value = element.findtext('active')
                if value is not None:
                    entry.static_active = True if value == 'yes' else False

                value = element.findtext('mandatory')
                if value is not None:
                    entry.static_mandatory = True if value == 'yes' else False

                value = element.findtext('group')
                if value is not None:
                    entry.group = value
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
            value=properties.findtext('sign')
            if value is not None:
                entry.print_sign = True if value == 'yes' else False
            value=properties.findtext('zeros')
            if value is not None:
                entry.leading_zeros = True if value == 'yes' else False

    def _inside_string(self, entry, element):
        properties = element.find('properties')
        if properties:
            value=properties.findtext('regexp')
            if value is not None:
                entry.reg_exp=value

    types = [
        EntryType('container', 'container-name', Container, _inside_container),
        EntryType('bool', 'entry-name', Bool),
        EntryType('string', 'entry-name', String, _inside_string),
        EntryType('fuzzy', 'entry-name', Fuzzy),
        EntryType('number', 'entry-name', Number, _inside_number)
    ]

