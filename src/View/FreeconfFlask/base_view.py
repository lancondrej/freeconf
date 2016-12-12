#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from flask import render_template
from flask_socketio import emit


__author__ = 'Ondřej Lanč'


class BaseView(object):
    """Base view class for Flask view in Freeconf.
    :param flask: Flask
    :param socketio Flask SocketIO
    """

    def __init__(self, flask, socketio):
        self._flask = flask
        self._socketio = socketio

    @staticmethod
    def render_default(title="", left="", main="", right=""):
        """default render function"""
        return render_template('index.html', title=title, left=left, main=main, right=right)

    @staticmethod
    def flash_message(message, category):
        """flash message through socketio, need to be catch by javascript"""
        flash = render_template('elements/flash.html', category=category, message=message)
        emit('flash', {'flash': flash},  namespace='/freeconf')

    @staticmethod
    def log(time, message):
        """send log message through socketio, need to be catch by javascript"""
        emit('log', {'log_time': time, 'log_record': message},  namespace='/freeconf')
