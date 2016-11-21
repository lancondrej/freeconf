#!/usr/bin/python3


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit
from flask_debugtoolbar import DebugToolbarExtension
from src.Presenter.main_presenter import MainPresenter
from src.View.Flask.main_view import MainView
from src.View.Flask.package_view import PackageView
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'


class FreeconfFlask(object):
    _renderer = Renderer()
    _flask = Flask(__name__)
    _socketio = SocketIO(_flask)
    _flask.jinja_env.autoescape = False

    def __init__(self, debug = False):
        self._presenter = MainPresenter()
        self._flask.debug = debug
        self._flask.config['SECRET_KEY'] = '56asdasss545'

        DebugToolbarExtension(self._flask)

        self._mainView=MainView(self._flask, self._socketio)
        self._packageView=PackageView(self._flask, self._socketio)

    def run(self):
        self._socketio.run(self._flask)