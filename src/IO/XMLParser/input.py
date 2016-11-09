#!/usr/bin/python3
#
import os

from src.Model.Package.package import Package
from src.IO.XMLParser.header_file import HeaderFileReader
from src.IO.XMLParser.list_file import ListFileReader
from src.IO.XMLParser.template_file import TemplateFileReader
from src.IO.input import Input
from src.IO.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class XMLParser(Input):
    def __init__(self, config, package):
        # configuration of package
        self.config = config
        # package itself
        self._package = package

    def load_package(self):
        self._load_header()
        self._load_lists()
        self._load_template()
        return self._package

    def _load_header(self):
        """Load header file. Support function for load_package."""
        HeaderFileReader(self.config).parse()

    def _load_lists(self, ):
        """Load list files."""
        ListFileReader(self.config, self._package).parse()

    def _load_template(self):
        """Load template file. Support function for load_package."""
        TemplateFileReader(self.config, self._package).parse()


    def load_plugin(self, plugins=None):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    def load_config(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError


    def load_packages_config(self):
        pass