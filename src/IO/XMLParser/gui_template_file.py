from src.IO.XMLParser.file_reader import FileReader
from src.IO.exception_logging.log import log
from src.Model.Package.entries.GUI.gwindow import GWindow
from src.Model.Package.entries.GUI.gtab import GTab
from src.Model.Package.entries.GUI.gsection import GSection
from src.Model.Package.package import Plugin

__author__ = 'Ondřej Lanč'


class GUITemplateFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        gui_template_file = self._config.gui_template_file
        log.info("Loading GUI template file {}".format(gui_template_file))
        super().__init__(gui_template_file)

    def parse(self):
        if isinstance(self._package, Plugin):
            window=self._package.package.gui_tree
        else:
            window = GWindow()
        for tab_element in self._root.iterfind('tab'):
            window.append(self._parse_tab(tab_element))
        self._package.gui_tree = window

    def _parse_tab(self, tab_element):
        tab = GTab()
        tab.name = tab_element.findtext('tab-name')
        tab.icon = tab_element.findtext('tab-icon')
        for section_element in tab_element.iterfind('tab-section'):
            tab.append(self._parse_tab_section(section_element))
        return tab

    def _parse_tab_section(self, section_element):
        section = GSection()
        section.name = section_element.findtext('tab-section-name')
        for entry_element in section_element.iterfind('import-entry'):
            name = entry_element.text
            if name:
                entry = self._package.tree.find_entry(name)
                section.append(entry)
        return section


