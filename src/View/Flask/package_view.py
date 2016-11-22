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
        self._flask.add_url_rule('/_multiple_modal', 'multiple_modal', self.multiple_modal)
        self._flask.add_url_rule('/_multiple_collapse', 'multiple_collapse', self.multiple_collapse)

        self._socketio.on_event('undo', self.undo, namespace='/freeconf')
        self._socketio.on_event('redo', self.redo, namespace='/freeconf')

        self._socketio.on_event('tab', self.tab, namespace='/freeconf')

        self._socketio.on_event('submit', self.submit, namespace='/freeconf')
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
        if self.presenter is not None:
            self.presenter.view = self
            session['package_name']=package_name
            sections = self.presenter.tab()
            rendered_sections = []
            for section in sections:
                rendered_sections.append(self._renderer.entry_render(section))
            main = render_template("package/tab.html", sections=rendered_sections)
            tabs = render_template("package/tabs.html", tabs=self.presenter.tabs, package_name=session.get('package_name'))
            buttons = render_template("package/buttons.html")
            return self.render_default(left=tabs, main=main, right=buttons)
        else:
            return self.render_default(main="error")

    def tab(self, data=None):
        self.presenter.tab(data['name'])

    def reload_tab(self, sections):
        rendered_sections=[]
        for section in sections:
            rendered_sections.append(self._renderer.entry_render(section))
        rendered_tab=render_template("package/tab.html", sections = rendered_sections)
        emit('reload_tab', {'rendered_tab': rendered_tab}, namespace='/freeconf')

    def reload_section(self, section):
        rendered_section=self._renderer.entry_render(section)
        emit('reload_section', {'full_name': section.full_name, 'rendered_section': rendered_section}, namespace='/freeconf')

    def reload_tabs(self, tabs):
        rendered_tabs=render_template("package/tabs.html", tabs = tabs, package_name=session.get('package_name'))
        emit('reload_tabs', {'rendered_tabs': rendered_tabs}, namespace='/freeconf')

    def multiple_modal(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_modal(entry)

    def multiple_collapse(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_collapse(entry)

    def reload_entry(self, entry):
        emit('reload_entry', {'full_name': entry.full_name, 'rendered_entry': self._renderer.reload_element(entry)}, namespace='/freeconf')

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
