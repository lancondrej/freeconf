#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

__author__ = 'Ondřej Lanč'


class FreeconfGeneralError(Exception):
    def __init__(self, message, logger=None):
        self.message = message
        self._print_to_log()
        self.logger = logger or logging.getLogger("Freeconf")

    def _print_to_log(self):
        if self.message is not None:
            self.logger.error(self._get_exception_header() + self.message)

    @staticmethod
    def _get_exception_header():
        return "General Freeconf error: "

    def __str__(self):
        return repr(self.message)