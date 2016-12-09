from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception import MissingMandatoryElementError
from src.IO.log import logger
from src.Model.Package.entries.bool import Bool
from src.Model.Package.entries.container import Container
from src.Model.Package.entries.fuzzy import Fuzzy
from src.Model.Package.entries.multiple.multiple_container import MultipleContainer
from src.Model.Package.entries.multiple.multiple_key_word import MultipleKeyWord
from src.Model.Package.entries.number import Number
from src.Model.Package.entries.string import String
from src.Model.Package.exception_logging.exception import AlreadyExistsError
from src.Model.Package.package import Plugin

__author__ = 'Ondřej Lanč'


class EntryType(object):
    def __init__(self, name, class_name, multiple,function=None):
        self.name = name
        self.class_name = class_name
        self.multiple_class = multiple
        self.inside_func = function


class TemplateFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        template_file = self._config.template_file
        logger.info("Loading template file {}".format(template_file))
        super().__init__(template_file)

    def parse(self):
        self._inside_container(self._package.tree, self._root)

    def _parse_entry(self, container_element):
        for element_type in self.types:
            for entry in self._parse_entry_of_type(container_element, element_type):
                yield entry

    def _parse_entry_of_type(self, container_element, element_type):
        for element in container_element.iterfind(element_type.name):
            name = element.get('name')
            if name:
                entry = element_type.class_name(name, self._package)
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
                # Entry properties
                # active
                value = element.findtext('active')
                if value is not None:
                    entry.static_active = True if value == 'yes' else False
                # group
                value = element.findtext('group')
                if value is not None:
                    entry.group=self._config.group(value)
                # other properties for specific type, and container recursion
                if element_type.inside_func:
                    element_type.inside_func(self, entry, element)
                yield entry
            else:
                raise MissingMandatoryElementError('{} name misssing'.format(element_type.name))



    def _inside_container(self, container, element):
        for entry in self._parse_entry(element):
            try:
                container.add_entry(entry)
            except AlreadyExistsError:
                pass

    def _inside_key_word(self, entry, element):
        # mandatory
        value = element.findtext('mandatory')
        if value is not None:
            entry.static_mandatory = True if value == 'yes' else False

    def _inside_number(self, entry, element):
        self._inside_key_word(entry, element)
        properties = element.find('properties')
        if properties is not None:
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
                entry.precision = int(value)
            value=properties.findtext('print_sign')
            if value is not None:
                entry.print_sign = True if value == 'yes' else False
            value=properties.findtext('leading_zeros')
            if value is not None:
                entry.leading_zeros = int(value)

    def _inside_string(self, entry, element):
        self._inside_key_word(entry, element)
        properties = element.find('properties')
        if properties is not None:
            value=properties.findtext('regexp')
            if value is not None:
                entry.reg_exp=value
            try:
                self._list(entry, properties)
            except AttributeError:
                logger.error("list not set")

    def _inside_fuzzy(self, entry, element):
        self._inside_key_word(entry, element)
        properties = element.find('properties')
        if properties is not None:
            self._list(entry, properties)

    def _list(self, entry, properties):
        data = properties.find('data')
        if data is not None:
            entry.user_values = True if data.get('strict') == 'no' else False
            value=data.text
            if value is not None:
                list = self._package.lists.get(value)
                if list is not None:
                    entry.list = list
                else:
                    raise AttributeError

    types = [
        EntryType('container', Container, MultipleContainer, _inside_container),
        EntryType('bool', Bool, MultipleKeyWord, _inside_key_word),
        EntryType('string', String, MultipleKeyWord, _inside_string),
        EntryType('fuzzy', Fuzzy, MultipleKeyWord, _inside_fuzzy),
        EntryType('number', Number, MultipleKeyWord, _inside_number)
    ]

