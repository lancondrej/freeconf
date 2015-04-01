#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'


from src.Model.exception_logging.log import log


class FcGeneralError (Exception):
    def __init__(self, message):
        self.message = message
        self._printToLog()

    def _printToLog(self):
        if self.message != None:
            log.error(self._getExceptionHeader() + self.message)

    def _getExceptionHeader(self):
        return "General error: "

    def __str__(self):
        return repr(self.message)


class FcParseError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader (self):
        return "Parse error: "


class FcPackageLoadError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader (self):
        return "Package load error: "


class FcTransformError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader(self):
        return "Transform error: "


class FcSaveError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader(self):
        return "Save error: "


class FcInconsistencyError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader(self):
        return "Inconsistency error: "


class FcAlreadyExistsError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader(self):
        return "Already exists: "


class FcNotExistsError (FcGeneralError):
    def __init__(self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader (self):
        return "Not exists: "


class FcMultipleError (FcGeneralError):
    def __init__ (self, message):
        FcGeneralError.__init__(self, message)

    def _getExceptionHeader (self):
        return "Not exists: "
