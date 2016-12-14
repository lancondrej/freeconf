#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template
from flask_socketio import emit

__author__ = 'Ondřej Lanč'


class BaseView(object):
    """Base view class for Flask view in Freeconf.

    :param freeconf: FreeconfFlask object
    """

    def __init__(self, freeconf):
        self._freeconf = freeconf
        self._flask = freeconf.flask
        self._socketio = freeconf.socketio
        self._main_presenter = freeconf.presenter

    @staticmethod
    def render_default(title="", left="", main="", right=""):
        """default render function"""
        return render_template('index.html', title=title, left=left, main=main,
                               right=right)

    @staticmethod
    def flash_message(message, category):
        """flash message through socketio, need to be catch by javascript"""
        flash = render_template('elements/flash.html', category=category,
                                message=message)
        emit('flash', {'flash': flash}, namespace='/freeconf')

    @staticmethod
    def log(time, message):
        """send log message through socketio, need to be catch by javascript"""
        emit('log', {'log_time': time, 'log_record': message},
             namespace='/freeconf')

    @property
    def main_presenter(self):
        """Main presenter getter
        :return MainPresenter
        """
        return self._main_presenter

    @main_presenter.setter
    def main_presenter(self, presenter):
        """package presenter setter"""
        self._main_presenter = presenter
