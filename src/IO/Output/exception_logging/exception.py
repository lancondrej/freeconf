#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

from IO.Input.exception_logging import log


class ParserGeneralError (Exception):
    def __init__(self, message):
        self.message = message
        self._printToLog()

    def _print_to_lo_log(self):
        if self.message is not None:
            log.error(self._get_exception_header() + self.message)

    def _get_exception_header(self):
        return "General error in parser: "

    def __str__(self):
        return repr(self.message)


class ParseError (ParserGeneralError):
    def __init__(self, message):
        ParserGeneralError.__init__(self, message)

    def _get_exception_header (self):
        return "Parse error: "



