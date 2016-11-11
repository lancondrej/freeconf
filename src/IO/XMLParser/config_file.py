import os
from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Config.group import Group
from src.Model.Package.lists import FuzzyList, StringList

__author__ = 'Ondřej Lanč'


class ConfigFileReader(FileReader):
    def __init__(self, config, package, config_file=None):
        self._config = config
        self._package = package
        list_file = config_file or self._config.config_file
        log.info("Loading List file {}".format(list_file))
        super().__init__(list_file)

    def parse(self):
        sl = self._parse_string_lists()
        fl = self._parse_fuzzy_list()
        self._package.lists = {**sl, **fl}

    def _parse_string_lists(self):
        return self._parse_list('string-list', StringList, self._string_value)

    def _parse_fuzzy_list(self):
        return self._parse_list('fuzzy-list', FuzzyList, self._fuzzy_value)

    def _parse_list(self, element, ListClass, value_func):
        list_elements = self._root.findall(element)
        lists={}
        for list_element in list_elements:
            log.info("List file: parsing <{}> element".format(element))
            name = list_element.get('name')
            if name:
                list = ListClass(name)
                for value in self._get_values(list_element, value_func):
                    list.append(value)
                lists[name]=list
            else:
                log.error("List file: in element <{}> missing attribute name".format(element))
        return lists

    @staticmethod
    def _get_values(element, value_func):
        values_element = element.findall('value')
        for value_element in values_element:
            yield value_func(value_element)

    @staticmethod
    def _string_value(element):
        return StringList.Entry(element.text)

    @staticmethod
    def _fuzzy_value(element):
        grade = element.get('grade')
        if grade:
            try:
                FuzzyList.Entry(grade, element.text)
            except AssertionError:
                log.error("Attribute grade={} is out of range for fuzzy value!".format(grade))
        else:
            log.error("Attribute grad missing")
