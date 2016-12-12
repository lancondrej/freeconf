#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.parse

import lxml.etree as etree

from src.IO.log import logger

__author__ = 'Ondřej Lanč'


class NativeFileWriter (object):
    def __init__(self, group, dom):
        self._group = group
        self._dom = dom

    def write_native(self):
        def _xsl_include(file):
            return '<xsl:include href="file://{}" />'.format(urllib.parse.quote(file))
        # Create XSL transformation
        xsl_string = '<?xml version="1.0" ?>' \
                     '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">'
        # Include main XSL file
        xsl_string += _xsl_include(self._group.transform_file)
        # Insert include
        for i in self._group.included_transforms:
            if i is not None:
                xsl_string += _xsl_include(i)
        xsl_string += '</xsl:stylesheet>'
        xslt_root = etree.XML(xsl_string)
        transform = etree.XSLT(xslt_root)
        newdom = transform(self._dom)
        f = open(self._group.native_output, 'w')
        f.write(str(newdom))
        logger.info("Writing output to {}".format(self._group.native_output))
