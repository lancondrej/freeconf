#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config

from src.View.FreeconfFlask.freeconf_flask import FreeconfFlask
_author__ = 'Ondřej Lanč'
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

if __name__ == '__main__':
    FreeconfFlask(debug=False).run()
