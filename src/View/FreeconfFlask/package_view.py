#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template, request, session, redirect, url_for
from flask_socketio import emit
from src.Presenter.main_presenter import MainPresenter
from src.View.FreeconfFlask.base_view import BaseView
from src.View.FreeconfFlask.renderer import Renderer

__author__ = 'Ondřej Lanč'


class PackageView(BaseView):
    """Main view for Freeconf. Attend to main pages of Freeconf.

    :param freeconf: FreeconfFlask object
    """

    def __init__(self, freeconf):
        BaseView.__init__(self, freeconf)
        self._renderer = Renderer()
        self._presenter = None

        self._flask.add_url_rule('/package/<package_name>', 'package',
                                 self.package)
        self._flask.add_url_rule('/_multiple_modal', 'multiple_modal',
                                 self.multiple_modal)
        self._flask.add_url_rule('/_multiple_collapse', 'multiple_collapse',
                                 self.multiple_collapse)

        self._socketio.on_event('undo', self.undo, namespace='/freeconf')
        self._socketio.on_event('redo', self.redo, namespace='/freeconf')

        self._socketio.on_event('tab', self.tab, namespace='/freeconf')

        self._socketio.on_event('submit', self.submit, namespace='/freeconf')
        self._socketio.on_event('multiple_new', self.multiple_new,
                                namespace='/freeconf')
        self._socketio.on_event('multiple_delete', self.multiple_delete,
                                namespace='/freeconf')
        self._socketio.on_event('multiple_up', self.multiple_up,
                                namespace='/freeconf')
        self._socketio.on_event('multiple_down', self.multiple_down,
                                namespace='/freeconf')
        self._socketio.on_event('save_config', self.save_config,
                                namespace='/freeconf')
        self._socketio.on_event('save_native', self.save_native,
                                namespace='/freeconf')

    @property
    def presenter(self):
        """package presenter getter"""
        # TODO: přidělovat presenter podle uživatelu (až bude)
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        """package presenter setter"""
        self._presenter = presenter

    def package(self, package_name=None):
        """method for load new package"""
        self.presenter = self.main_presenter.load_package(package_name)
        if self.presenter is not None:
            self.presenter.view = self
            session['package_name'] = package_name
            sections = self.presenter.active_tab.sections
            rendered_sections = []
            for section in sections:
                rendered_sections.append(self._renderer.entry_render(section))
            main = render_template("package/tab.html",
                                   sections=rendered_sections)
            tabs = render_template("package/tabs.html",
                                   tabs=self.presenter.tabs,
                                   package_name=session.get('package_name'))
            buttons = render_template("package/buttons.html")
            return self.render_default(title=self.presenter.label,
                                       left=tabs,
                                       main=main,
                                       right=buttons)
        else:
            return redirect(url_for('index'))

    def tab(self, data=None):
        """socketIO event for select tab"""
        self.presenter.tab(data['name'])

    def reload_tab(self, sections):
        """socketIO emit function for reload full tab, usually call from presenter"""
        rendered_sections = []
        for section in sections:
            rendered_sections.append(self._renderer.entry_render(section))
        rendered_tab = render_template("package/tab.html",
                                       sections=rendered_sections)
        emit('reload_tab',
             {'rendered_tab': rendered_tab},
             namespace='/freeconf')

    def reload_section(self, section):
        """socketIO emit function for reload section, usually call from presenter"""
        rendered_section = self._renderer.entry_render(section)
        emit('reload_section',
             {'full_name': section.full_name,
              'rendered_section': rendered_section},
             namespace='/freeconf')

    @staticmethod
    def reload_tabs(tabs):
        """socketIO emit function for reload tabs, usually call from presenter"""
        rendered_tabs = render_template("package/tabs.html",
                                        tabs=tabs,
                                        package_name=session.get(
                                            'package_name'))
        emit('reload_tabs',
             {'rendered_tabs': rendered_tabs},
             namespace='/freeconf')

    def multiple_modal(self):
        """render modal window"""
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_modal(entry)

    def multiple_collapse(self):
        """render collapse multiple"""
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_collapse(entry)

    def reload_entry(self, entry):
        """socketIO emit function for reload entry, usually call from presenter"""
        emit('reload_entry',
             {'full_name': entry.full_name,
              'rendered_entry': self._renderer.reload_element(entry)},
             namespace='/freeconf')

    def submit(self, data):
        """socketIO event for submit"""
        full_name = data['full_name']
        value = data['value']
        self.presenter.save_value(full_name, value)

    def multiple_new(self, data):
        """socketIO event for multiple new"""
        full_name = data['full_name']
        self.presenter.multiple_new(full_name)

    def multiple_delete(self, data):
        """socketIO event for multiple delete"""
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_delete(full_name, value)

    def multiple_up(self, data):
        """socketIO event for multiple up"""
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_up(full_name, value)

    def multiple_down(self, data):
        """socketIO event for multiple down"""
        full_name = data['full_name']
        value = data['value']
        self.presenter.multiple_down(full_name, value)

    def undo(self):
        """socketIO event for undo"""
        self.presenter.undo()

    def redo(self):
        """socketIO event for redo"""
        self.presenter.redo()

    def save_config(self):
        """socketIO event for save configuration"""
        self.presenter.save_config()

    def save_native(self):
        """socketIO event for save native"""
        self.presenter.save_native()
