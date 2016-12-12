#!/usr/bin/python3
# -*- coding: utf-8 -*-#

from flask import render_template, redirect, url_for
from src.Presenter.main_presenter import MainPresenter
from src.View.FreeconfFlask.base_view import BaseView

__author__ = 'Ondřej Lanč'


class MainView(BaseView):
    """Main view for Freeconf.
    Attend to main pages of Freeconf.
    :param flask: Flask object
    :param socketio: SocketIO object
    """
    def __init__(self, flask, socketio):
        BaseView.__init__(self, flask, socketio)
        self._presenter = MainPresenter()
        self._presenter.view = self
        self._flask.add_url_rule('/', 'index', self.index)
        self._flask.add_url_rule('/about', 'about', self.about)
        self._flask.add_url_rule('/configure', 'configure', self.configure)
        self._flask.add_url_rule('/setting', 'setting', self.setting)

        self._socketio.on_event('reload_config', self.reload_config, namespace='/freeconf')

    def index(self):
        """dafault page at /"""
        return self.render_default()

    @property
    def presenter(self):
        """main presenter getter"""
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        """main presenter setter
        :param presenter
        """
        self._presenter = presenter

    @staticmethod
    def setting():
        """setting page redirect to package view for self Freeconf package"""
        return redirect(url_for('package', package_name='freeconf'))

    def about(self):
        """page about"""
        self._flask.update_template_context({'body': render_template("about.html")})
        return render_template('index.html')

    def configure(self):
        """page with list of available packages"""
        packages = self.presenter.config.packages_list
        return self.render_default(main=render_template("configure.html", packages=packages))

    def reload_config(self):
        """socketIO event for redo"""
        self.presenter.reload_config()
