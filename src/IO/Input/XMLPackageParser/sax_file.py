#!/usr/bin/python
#
# sax_file.py
# begin: 3.8.2010 by Jan Ehrenberger
#
# Base file for SAX parsers
#

import xml.sax
import xml.sax.handler

from src.IO.Input.exception_logging.exception import ParseError


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
            raise ParseError(e.getMessage())