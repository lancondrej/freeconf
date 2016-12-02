from src.IO.XMLParser.file_reader import FileReader
from src.IO.log import logger


__author__ = 'Ondřej Lanč'


class ListHelpFileReader(FileReader):
    def __init__(self, config, package, language):
        self._config = config
        self._package = package
        list_help_file = self._config.list_help_file(language)
        logger.info("Loading List help file {}".format(list_help_file))
        super().__init__(list_help_file)

    def parse(self):
        self._parse_string_lists()
        self._parse_fuzzy_list()

    def _parse_string_lists(self):
        return self._parse_list('string-list')

    def _parse_fuzzy_list(self):
        return self._parse_list('fuzzy-list')

    def _parse_list(self, element):
        for list_element in self._root.iterfind(element):
            logger.info("List file: parsing <{}> element".format(element))
            name = list_element.get('name')
            if name:
                try:
                    list=self._package.lists[name]
                    self._parse_entry(list, list_element)
                except KeyError:
                    logger.error("No list {} in package".format(name))
            else:
                logger.error("List file: in element <{}> missing attribute name".format(element))

    def _parse_entry(self, list, list_element):
        for entry in list_element.iterfind('entry'):
            value = entry.get('value')
            if value:
                list_entry = list.get_entry(value)
                if list_entry is not None:
                    list_entry.label = entry.findtext('label')
                    list_entry.help = entry.findtext('help')
            else:
                logger.error("list entry name not defined")
