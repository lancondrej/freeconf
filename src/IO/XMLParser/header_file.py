from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Config.group import Group

__author__ = 'Ondřej Lanč'


class HeaderFileReader(FileReader):
    def __init__(self, config):
        self._config = config
        header_file = self._config.header_file
        log.info("Loading header file {}".format(header_file))
        super().__init__(header_file)

    def parse(self):
        # self.parse_package_info()
        self.parse_content()
        self.parse_group()

    def parse_content(self):
        content_element = self._root.find('content')
        if content_element:
            log.info("Header file: parsing <content> element")
            self._config.file.template = content_element.findtext('template')
            self._config.file.output = content_element.findtext('output')
            self._config.file.default_values = content_element.findtext('default-values')
            self._config.file.help = content_element.findtext('help')
            self._config.file.output = content_element.findtext('output')
            self._config.file.dependencies = content_element.findtext('dependencies')
            self._config.file.gui_template = content_element.findtext('gui-template')
            self._config.file.gui_label = content_element.findtext('gui-label')
            self._config.file.list = content_element.findtext('lists')
        else:
            raise ParseError("Header file: element <content> missing")

    def parse_group(self):
        group_elements = self._root.findall('entry-group')
        if not group_elements:
            raise ParseError("Header file: element <entry-group> missing")
        for group_element in group_elements:
            log.info("Header file: parsing <entry-group> element")
            name = group_element.get('name')
            group=Group(name)
            group.transform = group_element.findtext('transform')
            group.native_output = group_element.findtext('native-output')
            group.output_defaults = group_element.findtext('output-defaults')
            self._config.add_group(group)

    def parse_package_info(self):
        package_info_element = self._root.find('package-info')
        if package_info_element:
            log.info("Header file: parsing <package-info> element")
        else:
            log.info("Header file: element <package-info> missing")
