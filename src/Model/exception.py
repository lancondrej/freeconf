#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from src.exception import FreeconfGeneralException

__author__ = 'Ondřej Lanč'


class ModelGeneralException(FreeconfGeneralException):
    def __init__(self, message):
        super.__init__(message, logging.getLogger("Model"))

    def _get_exception_header(self):
        return "General error in Model: "


class IncompatibleListTypeException(ModelGeneralException):
    def __init__(self, message):
        ModelGeneralException.__init__(self, message)

    def _get_exception_header(self):
        return "Incompatible list type!: "

class PropertyException(ModelGeneralException):
    def __init__(self, message):
        ModelGeneralException.__init__(self, message)

    def _get_exception_header(self):
        return "Property setting problem: "

class AlreadyExistsException(ModelGeneralException):
    def __init__(self, message):
        ModelGeneralException.__init__(self, message)

    def _get_exception_header(self):
        return "Already exist: "
