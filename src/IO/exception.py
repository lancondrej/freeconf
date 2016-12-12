#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from src.exception import FreeconfGeneralException

__author__ = 'Ondřej Lanč'


class IOGeneralException (FreeconfGeneralException):
    def __init__(self, message):
        super.__init__(message, logging.getLogger("IO"))

    def _get_exception_header(self):
        return "General error in IO: "


class MissingMandatoryElementException (IOGeneralException):
    def __init__(self, message):
        IOGeneralException.__init__(self, message)

    def _get_exception_header(self):
        return "Mandatory element missing or is empty: "



