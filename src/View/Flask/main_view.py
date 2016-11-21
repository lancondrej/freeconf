#!/usr/bin/python3


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit
from flask_debugtoolbar import DebugToolbarExtension
from src.Presenter.main_presenter import MainPresenter
from src.View.Flask.base_view import BaseView
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'


class MainView(BaseView):
    def __init__(self, flask, socketio):
        self._presenter = MainPresenter()
        self._flask = flask
        self._socketio = socketio

        self._flask.add_url_rule('/', 'index', self.index)
        self._flask.add_url_rule('/about', 'about', self.about)
        self._flask.add_url_rule('/configure', 'configure', self.configure)
        self._flask.add_url_rule('/setting', 'setting', self.setting)

    def index(self):
        return self.render_default()

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter=presenter

    def setting(self):
        return "baf"

    def about(self):
        self._flask.update_template_context({'body': render_template("about.html")})
        return render_template('index.html')
        # return self.render_default(body= render_template("about.html"))

    def configure(self):
        packages=self.presenter.config.packages_list
        return self.render_default(body= render_template("configure.html", packages=packages))

    def render_default(self, tabs=None, body=""):
        return render_template('index.html', package_name=session.get('package_name'), tabs=tabs, main=body)
