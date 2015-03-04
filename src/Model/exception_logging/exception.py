#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


from src.Model.exception_logging.log import log


class FcModelGeneralError (Exception):
    def __init__(self, message):
        self.message = message
        self._print_to_log()

    def _print_to_log(self):
        if self.message is not None:
            log.error(self._get_exception_header() + self.message)

    def _get_exception_header(self):
        return "General error in Model: "

    def __str__(self):
        return repr(self.message)


class FcPackageLoadError (FcModelGeneralError):
    def __init__(self, message):
        FcModelGeneralError.__init__(self, message)

    def _get_exception_header(self):
        return "Package load error: "



