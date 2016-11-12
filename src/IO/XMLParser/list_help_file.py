import os
from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Config.group import Group
from src.Model.Package.lists import FuzzyList, StringList

__author__ = 'Ondřej Lanč'


class ListHelpFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        list_help_file = self._config.list_help_file
        log.info("Loading List help file {}".format(list_help_file))
        super().__init__(list_help_file)

    def parse(self):
        self._parse_string_lists()
        self._parse_fuzzy_list()

    def _parse_string_lists(self):
        return self._parse_list('string-list')

    def _parse_fuzzy_list(self):
        return self._parse_list('fuzzy-list')

    def _parse_list(self, element):
        list_elements = self._root.findall(element)
        for list_element in list_elements:
            log.info("List file: parsing <{}> element".format(element))
            name = list_element.get('name')
            if name:
                try:
                    list=self._package.lists[name]
                    self._parse_entry(list, list_element)
                except KeyError:
                    log.error("No list {} in package".format(name))
            else:
                log.error("List file: in element <{}> missing attribute name".format(element))

    def _parse_entry(self, list, list_element):
        entries=list_element.findall('entry')
        for entry in entries:
            value = entry.findtext('value')
            if value is not None:
                list_entry = list.get_entry(value)
                if list_entry is not None:
                    list_entry.label = entry.findtext('label')
                    list_entry.help = entry.findtext('help')
            else:
                log.error("list entry name not defined")
