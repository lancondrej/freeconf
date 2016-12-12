#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

__author__ = 'Ondřej Lanč'

class ModelGeneralError(Exception):
    def __init__(self, message, logger=None):
        self.message = message
        self._print_to_log()
        self.logger = logger or logging.getLogger("Model")

    def _print_to_log(self):
        if self.message is not None:
            self.logger.error(self._get_exception_header() + self.message)

    def _get_exception_header(self):
        return "General error in Model: "

    def __str__(self):
        return repr(self.message)


class PackageLoadError(ModelGeneralError):
    def __init__(self, message):
        ModelGeneralError.__init__(self, message)

    def _get_exception_header(self):
        return "Package load error: "


class MultipleError(ModelGeneralError):
    def __init__(self, message):
        ModelGeneralError.__init__(self, message)

    def _get_exception_header(self):
        return "Not exists: "


class AlreadyExistsError(ModelGeneralError):
    def __init__(self, message):
        ModelGeneralError.__init__(self, message)

    def _get_exception_header(self):
        return "Already exist: "


class NotExistsError(ModelGeneralError):
    def __init__(self, message):
        ModelGeneralError.__init__(self, message)

    def _get_exception_header(self):
        return "Not exist: "


class InconsistencyError (ModelGeneralError):
    def __init__ (self, message):
        ModelGeneralError.__init__(self, message)

    def _get_exception_header (self):
        return "Inconsistency error: "