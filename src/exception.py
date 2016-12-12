#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

__author__ = 'Ondřej Lanč'


class FreeconfGeneralException(Exception):
    def __init__(self, message, logger=None):
        self.message = message
        self.logger = logger or logging.getLogger("Freeconf")
        self._print_to_log()

    def _print_to_log(self):
        if self.message is not None:
            self.logger.error(self._get_exception_header() + self.message)

    def _get_exception_header(self):
        return "General Freeconf error: "

    def __str__(self):
        return repr(self.message)
