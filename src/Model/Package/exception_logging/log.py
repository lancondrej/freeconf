#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

__author__ = 'Ondřej Lanč'


# Setup logging to stderr
handler = logging.StreamHandler()
format = logging.Formatter("ModelLog %(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(format)

# Create log object
log = logging.getLogger('Model-Freeconf')
log.addHandler(handler)
log.setLevel(logging.ERROR)
