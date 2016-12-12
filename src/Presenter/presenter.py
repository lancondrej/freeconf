#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from src.Presenter.log import logger
import time

__author__ = 'Ondřej Lanč'

class Presenter(object):

    def __init__(self):
        self.view = None

    def log(self, message):
        localtime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        logger.debug(message)
        self.view.log(localtime, message)