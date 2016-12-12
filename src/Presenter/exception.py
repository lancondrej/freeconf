#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from src.Presenter.log import logger

__author__ = 'Ondřej Lanč'


class PresenterGeneralError (Exception):
    def __init__(self, message):
        self._message = message
        self._print_to_lo_log()

    def _print_to_lo_log(self):
        if self._message is not None:
            logger.error(self._get_exception_header() + self._message)

    def _get_exception_header(self):
        return "General error in parser: "

    def __str__(self):
        return repr(self._message)


# class MissingMandatoryElementError (ViewGeneralError):
#     def __init__(self, message):
#         PresenterGeneralError.__init__(self, message)
#
#     def _get_exception_header(self):
#         return "Mandatory element missing or is empty: "



