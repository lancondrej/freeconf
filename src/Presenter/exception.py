#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from src.exception import FreeconfGeneralException

__author__ = 'Ondřej Lanč'


class PresenterGeneralError(FreeconfGeneralException):
    def __init__(self, message):
        super.__init__(message, logging.getLogger("Presenter"))

    def _get_exception_header(self):
        return "General error in Presenter: "
