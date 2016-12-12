#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import time

__author__ = 'Ondřej Lanč'


class Presenter(object):
    def __init__(self):
        self.view = None
        self.logger = logging.getLogger("Presenter")

    def log(self, message):
        localtime = time.strftime('%Y/%m/%d %H:%M:%S',
                                  time.localtime(time.time()))
        self.logger.debug(message)
        self.view.log(localtime, message)
