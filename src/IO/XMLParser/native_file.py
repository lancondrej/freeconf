import urllib.parse
import lxml.etree as ET

from src.IO.XMLParser.config_file import ConfigFileWriter
from src.IO.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class NativeFileWriter (object):
    def __init__(self, group, dom):
        self._group = group
        self._dom = dom

    def write_native(self):



        # Create XSL transformation
        xslString = '<?xml version="1.0" ?>' \
                    '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">'
        # Include main XSL file
        xslString += '<xsl:include href="file://{}" />'.format(urllib.parse.quote(self._group.transform_file))

        # Insert include
        for i in self._group.included_transforms:
            if i is not None:
                xslString += '<xsl:include href="file://{}" />'.format(urllib.parse.quote(i))


        xslString += '</xsl:stylesheet>'




        # xslt = ET.parse(self._group.transform_file)

        xslt=ET.XML(xslString)
        transform = ET.XSLT(xslt)
        newdom = transform(self._dom)
        f = open(self._group.native_output, 'w')
        f.write(str(newdom))
        log.info("Witing output to {}".format(self._group.native_output))
