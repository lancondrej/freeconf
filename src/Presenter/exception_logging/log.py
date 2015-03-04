#!/usr/bin/python3
#
__author__ = 'Ondřej Lanč'

import logging

# Setup logging to stderr
handler = logging.StreamHandler()
format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
handler.setFormatter(format)

# Create log object
log = logging.getLogger('PyFreeconf')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

