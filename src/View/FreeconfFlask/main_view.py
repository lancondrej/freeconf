#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from src.Presenter.main_presenter import MainPresenter
from src.View.FreeconfFlask.base_view import BaseView

__author__ = 'Ondřej Lanč'


class MainView(BaseView):
    """Main view for Freeconf.

    :param freeconf: FreeconfFlask object
    """

    def __init__(self, freeconf, ):
        BaseView.__init__(self, freeconf)
        self._main_presenter.view = self
        self._flask.add_url_rule('/', 'index', self.index)
        self._flask.add_url_rule('/docu', 'docu', self.documentation)
        self._flask.add_url_rule('/configure', 'configure', self.configure)
        self._flask.add_url_rule('/setting', 'setting', self.setting)
        self._flask.add_url_rule('/_shutdown', 'shutdown', self.shutdown)

        self._socketio.on_event('reload_config', self.reload_config,
                                namespace='/freeconf')

    def index(self):
        """function for default page at url /"""
        return self.render_default()

    @property
    def presenter(self):
        """main presenter getter"""
        return self._main_presenter

    @presenter.setter
    def presenter(self, presenter):
        """main presenter setter

        :param presenter: Main presenter
        """
        self._main_presenter = presenter

    @staticmethod
    def setting():
        """setting page redirect to package view for self Freeconf package"""
        return redirect(url_for('package', package_name='freeconf'))

    def documentation(self):
        """page about"""
        return self.render_default(main=render_template("doc.html"))

    def configure(self):
        """page with list of available packages"""
        packages = self.presenter.config.packages_list
        return self.render_default(main=render_template("configure.html",
                                                        packages=packages))

    def reload_config(self):
        """socketIO event for redo"""
        self.presenter.reload_config()

    def shutdown(self):
        """shutdown socketio server"""
        self._freeconf.shutdown_server()

