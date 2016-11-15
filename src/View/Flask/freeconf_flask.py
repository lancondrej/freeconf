#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# app = Flask(__name__)
# app.config.from_object(__name__)
# app.jinja_env.autoescape = False
# app.secret_key = 'some_secret'
# app.debug = True
# toolbar = DebugToolbarExtension(app)
# app.config['DEBUG_TB_PROFILER_ENABLED'] = True
from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'


class FreeconfFlask(Flask):
    def __init__(self, name, **kwargs):
        super(FreeconfFlask, self).__init__(name, **kwargs)
        self._presenter = None
        self._renderer = Renderer()
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/about', 'about', self.about)
        self.add_url_rule('/setting', 'setting', self.setting)
        self.add_url_rule('/package/<name>', 'package', self.package)
        self.add_url_rule('/tab/<name>', 'tab', self.tab)

        self.add_url_rule('/_multiple_new', 'multiple_new', self.multiple_new)
        self.add_url_rule('/_multiple_delete', 'multiple_delete', self.multiple_delete)
        self.add_url_rule('/_multiple_up', 'multiple_up', self.multiple_up)
        self.add_url_rule('/_multiple_down', 'multiple_down', self.multiple_down)
        self.add_url_rule('/_multiple_modal', 'multiple_modal', self.multiple_modal)
        self.add_url_rule('/_multiple_collapse', 'multiple_collapse', self.multiple_collapse)

        self.add_url_rule('/_reload_element', 'reload_element', self.reload_element)
        self.add_url_rule('/_flash', 'flash_message', self.flash_message)
        self.add_url_rule('/_submit', 'submit', self.submit)
        self.add_url_rule('/configure', 'configure', self.configure)
        self.add_url_rule('/_save_config', 'save_config', self._save_config)
        self.add_url_rule('/_save_native', 'save_native', self._save_native)

        self.add_url_rule('/_undo', 'undo', self._undo)
        self.add_url_rule('/_redo', 'redo', self._redo)

        # app.add_url_rule('/users/', view_func=ShowUsers.as_view('show_users'))

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, presenter):
        self._presenter=presenter

    def setting(self):
        return self.package("Freeconf")

    def about(self):
        return self.render_default(body= render_template("about.html"))

    def configure(self):
        packages=self.presenter.config.packages_list
        return self.render_default(body= render_template("configure.html", packages=packages))

    def render_default(self, package=None, tabs=None, body=""):
        return render_template('index.html', package_name=package, tabs=tabs, main=body)

    def package(self, name):
        if self.presenter.load_package(name):
            return self.render_default(package=self.presenter.package.package_name, tabs=self.presenter.package.tabs())
        else:
            return "error"

    def submit(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.entry.save_value(full_name, value)
        return jsonify(result=value)

    def tab(self, name):
        sections = self.presenter.package.tab(name)
        Rsection = ""
        for section in sections:
            Rsection = Rsection + self._renderer.entry_render(section)
        return self.render_default(tabs = self.presenter.package.tabs(), body = Rsection)

    def index(self):
        return self.render_default()

    def multiple_new(self):
        full_name = request.args.get('full_name')
        result = self.presenter.entry.multiple_new(full_name)
        if result is None:
            flash(u'Maximum element reach', 'warning')
        return jsonify(result=result)

    def multiple_delete(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        result = self.presenter.entry.multiple_delete(full_name, value)
        if result is None:
            flash(u'Minimum element reach', 'warning')
        return jsonify(result=result)

    def multiple_up(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.entry.multiple_up(full_name, value)
        return ""

    def multiple_down(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.entry.multiple_down(full_name, value)
        return ""

    def multiple_modal(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.entry.get_entry(full_name)
        return self._renderer.render_modal(entry)

    def multiple_collapse(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.entry.get_entry(full_name)
        return self._renderer.render_collapse(entry)

    def reload_element(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.entry.get_entry(full_name)
        return self._renderer.reload_element(entry)

    def flash_message(self):
        return render_template('elements/flash.html')

    def _save_config(self):
        result = self.presenter.package.save_config()
        if result:
            flash(u'Configuration save', 'success')
        else:
            flash(u'Configuration not save', 'danger')
        return redirect(url_for('package', name=self.presenter.package.package_name))

    def _save_native(self):
        result = self.presenter.package.save_native()
        if result:
            flash(u'NAtive configuration save', 'success')
        else:
            flash(u'Native Configuration not save', 'danger')
        return redirect(url_for('package', name=self.presenter.package.package_name))

    def _undo(self):
        undo = self.presenter.package.undo.undo()
        return jsonify(result=(undo is not None), full_name=undo)

    def _redo(self):
        redo = self.presenter.package.undo.redo()
        return jsonify(result=(redo is not None), full_name=redo)
