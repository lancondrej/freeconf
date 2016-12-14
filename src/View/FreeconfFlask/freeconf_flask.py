#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_socketio import SocketIO
from src.Presenter.main_presenter import MainPresenter
from src.View.FreeconfFlask.main_view import MainView
from src.View.FreeconfFlask.package_view import PackageView

__author__ = 'Ondřej Lanč'


class FreeconfFlask(object):
    """View class for Freeconf. Have as property Flask and SocketiIO object.

    :param debug: bool
    """

    def __init__(self, debug=False):
        self.flask = Flask(__name__)
        self.socketio = SocketIO(self.flask)
        self.presenter = MainPresenter()
        self.flask.debug = debug
        self.flask.config['SECRET_KEY'] = '56asdasss545'
        self.flask.config['TEMPLATES_AUTO_RELOAD'] = True
        # main view
        self._mainView = MainView(self)
        # view for package
        self._packageView = PackageView(self)

    def run(self, host=None, port=None):
        """main method for run server from Flask and SocketIO
        :param host: The hostname or IP address for the server to listen on.
                    Defaults to 127.0.0.1.
        :param port: The port number for the server to listen on. Defaults
                    to 5000.
        """
        self.socketio.run(self.flask, host=host, port=port)
