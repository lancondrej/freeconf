#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

import xml.sax
from src.PackageParser.exception_logging.exception import FcXmlParserGeneralError


class XMLFileReader(xml.sax.handler.ContentHandler):
    # values_true = ("yes", "true", "1")
    # values_false = ("no", "false", "0")

    def __init__(self):
        # Flag for file being enclosed in right tags
        self.enclosing_tag = False

    def parse(self, file):
        try:
            xml.sax.parse(file, self)
        except xml.sax.SAXParseException as e:
            raise FcXmlParserGeneralError(e.getMessage())

