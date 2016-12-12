#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from src.IO.XMLParser.file_reader import FileReader
from src.IO.log import logger
from src.Model.Package.lists.fuzzy_list import FuzzyList
from src.Model.Package.lists.string_list import StringList

__author__ = 'Ondřej Lanč'


class ListFileReader(FileReader):
    def __init__(self, config, package):
        self._config = config
        self._package = package
        list_file = self._config.list_file
        logger.info("Loading List file {}".format(list_file))
        super().__init__(list_file)

    def parse(self):
        sl = self._parse_string_lists()
        fl = self._parse_fuzzy_list()
        self._package.lists = {**sl, **fl}

    def _parse_string_lists(self):
        return self._parse_list('string_list', StringList, self._string_value)

    def _parse_fuzzy_list(self):
        return self._parse_list('fuzzy_list', FuzzyList, self._fuzzy_value)

    def _parse_list(self, element, ListClass, value_func):
        lists={}
        for list_element in self._root.iterfind(element):
            logger.info("List file: parsing <{}> element".format(element))
            name = list_element.get('name')
            if name:
                list = ListClass(name)
                for value in self._get_values(list_element, value_func):
                    list.append(value)
                lists[name]=list
            else:
                logger.error("List file: in element <{}> missing attribute name".format(element))
        return lists

    @staticmethod
    def _get_values(element, value_func):
        for value_element in element.iterfind('value'):
            yield value_func(value_element)

    @staticmethod
    def _string_value(element):
        return StringList.Entry(element.text)

    @staticmethod
    def _fuzzy_value(element):
        grade = element.get('grade')
        if grade is not None:
            try:
                return FuzzyList.Entry(float(grade), element.text)
            except AssertionError:
                logger.error("Attribute grade={} is out of range for fuzzy value!".format(grade))
        else:
            logger.error("Attribute grade missing")
