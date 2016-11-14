from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.IO.exception_logging.exception import ParseError
from src.Model.Config.group import Group
from src.Model.Config.package import Plugin, Package

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
        group_not_set=True

        for group_element in self._root.iterfind('entry-group'):
            log.info("Header file: parsing <entry-group> element")
            name = group_element.get('name')
            group=Group(name)
            group.transform_file = group_element.findtext('transform')
            group._native_output = group_element.findtext('native-output')
            group.output_defaults = True if group_element.findtext('output-defaults') == 'yes' else False
            self._config.add_group(group)
            group_not_set=False

        if isinstance(self._config, Plugin):
            for group_element in self._root.iterfind('change-group'):
                log.info("Header file: parsing <change-group> element")
                name = group_element.get('name')
                group=self._config.parent.group(name)
                if group:
                    group.include_transform(group_element.findtext('add-transform'))
                else:
                    log.error("group name {} is not in Package".format(name))

        else:
            if group_not_set:
                log.warning("Header file: element <entry-group> missing")
                log.info("Creating default group")
                group = Group("default")
                self._config.add_group(group)

    def parse_package_info(self):
        package_info_element = self._root.find('package-info')
        if package_info_element:
            log.info("Header file: parsing <package-info> element")
        else:
            log.info("Header file: element <package-info> missing")

