#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

import logging

# Setup logging to stderr
handler = logging.StreamHandler()
format = logging.Formatter("InputLog %(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(format)

# Create log object
log = logging.getLogger('Input')
log.addHandler(handler)
log.setLevel(logging.ERROR)
