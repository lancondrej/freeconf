#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

__author__ = 'Ondřej Lanč'


# Create log object
logger = logging.getLogger('IO')
logger.setLevel(logging.DEBUG)

# Setup logging to stderr
handler = logging.StreamHandler()
format = logging.Formatter("IOLog %(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(format)

logger.addHandler(handler)




