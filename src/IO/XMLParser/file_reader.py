#!/usr/bin/python3
# -*- coding: utf-8 -*-#

import xml.etree.ElementTree as ET

__author__ = 'Ondřej Lanč'


class FileReader(object):

    def __init__(self, file):
        if file is None:
            raise FileExistsError("file missing")
        self._file=file
        self._root = self._get_root()

    def _get_root(self):
        try:
            return ET.parse(self._file).getroot()
        except FileNotFoundError:
            raise FileExistsError("file missing")

    def parse(self):
        raise NotImplementedError
