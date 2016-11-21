#!/usr/bin/python3


from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Blueprint
from flask_socketio import SocketIO, emit
from flask_debugtoolbar import DebugToolbarExtension
from src.Presenter.main_presenter import MainPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.View.Flask.base_view import BaseView
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'



class PackageView(BaseView):
    _renderer = Renderer()

    def __init__(self, flask, socketio):
        self._flask = flask
        self._socketio = socketio
        self._presenter = None

        self._flask.add_url_rule('/<package_name>', 'package', self.package)
        self._flask.add_url_rule('/<package_name>/<tab_name>', 'tab', self.tab)
        self._flask.add_url_rule('/_multiple_modal', 'multiple_modal', self.multiple_modal)
        self._flask.add_url_rule('/_multiple_collapse', 'multiple_collapse', self.multiple_collapse)

        self._socketio.on_event('submit', self.submit, namespace='/freeconf')
        self._socketio.on_event('undo', self.undo, namespace='/freeconf')
        self._socketio.on_event('redo', self.redo, namespace='/freeconf')
        self._socketio.on_event('multiple_new', self.multiple_new, namespace='/freeconf')
        self._socketio.on_event('multiple_delete', self.multiple_delete, namespace='/freeconf')
        self._socketio.on_event('multiple_up', self.multiple_up, namespace='/freeconf')
        self._socketio.on_event('multiple_down', self.multiple_down, namespace='/freeconf')
        self._socketio.on_event('save_config', self.save_config, namespace='/freeconf')
        self._socketio.on_event('save_native', self.save_native, namespace='/freeconf')

    @property
    def presenter(self):
        # TODO: přidělovat presenter podle uživatelu (až bude)
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter=presenter

    def package(self, package_name):
        self.presenter = MainPresenter.load_package(package_name)
        self.presenter.view = self
        if self.presenter is not None:
            session['package_name']=package_name
            return self.tab(package_name)
        else:
            return "error"

    def render_default(self, tabs=None, body=""):
        return render_template('index.html', package_name=session.get('package_name'), tabs=tabs, main=body)

    def tab(self, package_name, tab_name=None):
        sections = self.presenter.tab(tab_name)
        Rsection = ""
        for section in sections:
            Rsection = Rsection + self._renderer.entry_render(section)
        return self.render_default(tabs = self.presenter.tabs(), body = Rsection)

    def multiple_modal(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_modal(entry)

    def multiple_collapse(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_collapse(entry)

    def reload_entry(self, entry):
        emit('reload', {'full_name': entry.full_name, 'rendered_entry': self._renderer.reload_element(entry)}, namespace='/freeconf')

    def submit(self, data):
        full_name = data['full_name']
        value = data['value']
        self.presenter.save_value(full_name, value)

    def multiple_new(self, data):
        full_name = data['full_name']
        self.presenter.multiple_new(full_name)

    def multiple_delete(self, data):
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_delete(full_name, value)

    def multiple_up(self, data):
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_up(full_name, value)

    def multiple_down(self, data):
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_down(full_name, value)

    def undo(self):
        self.presenter.undo()

    def redo(self):
        self.presenter.redo()

    def save_config(self):
        self.presenter.save_config()

    def save_native(self):
        self.presenter.save_native()
