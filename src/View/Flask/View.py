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


class FreeconfView(Flask):
    def __init__(self, import_name, **kwargs):
        super(FreeconfView, self).__init__(import_name, **kwargs)
        self._presenter = PackagePresenter()
        self._renderer = Renderer()
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/about', 'about', self.about)
        self.add_url_rule('/setting', 'setting', self.setting)
        self.add_url_rule('/package/<name>', 'package', self.package)
        self.add_url_rule('/package/<package>/<name>/', 'tab', self.tab)
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
        # self.add_url_rule('/', 'index', self.index)

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
        packages=self.presenter.packages
        return self.render_default(body= render_template("configure.html", packages=packages))

    def render_default(self, tabs=None, body=""):
        return render_template('index.html', package_name=self.presenter.package_name, tabs=tabs, main=body)

    def package(self, name):
        if self.presenter.load_package(name):
            return self.render_default(tabs=self.presenter.tabs())
        else:
            return "error"

    def submit(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.save_value(full_name, value)
        return jsonify(result=value)

    def tab(self, package, name):
        if self.presenter.package_name != package:
            self.package(package)
        sections = self.presenter.tab(name)
        Rsection = ""
        for section in sections:
            Rsection = Rsection + self._renderer.entry_render(section)
        return self.render_default(tabs = self.presenter.tabs(), body = Rsection)

    def index(self):
        return self.render_default()

    def multiple_new(self):
        full_name = request.args.get('full_name')
        result = self.presenter.multiple_new(full_name)
        if not result:
            flash(u'Maximum element reach', 'warning')
        return jsonify(result=result)

    def multiple_delete(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        result = self.presenter.multiple_delete(full_name, value)
        if not result:
            flash(u'Minimum element reach', 'warning')
        return jsonify(result=result)

    def multiple_up(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.multiple_up(full_name, value)
        return ""

    def multiple_down(self):
        full_name = request.args.get('full_name')
        value = request.args.get('value')
        self.presenter.multiple_down(full_name, value)
        return ""

    def multiple_modal(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_modal(entry)

    def multiple_collapse(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.render_collapse(entry)

    def reload_element(self):
        full_name = request.args.get('full_name')
        entry = self.presenter.get_entry(full_name)
        return self._renderer.reload_element(entry)

    def flash_message(self):
        return render_template('elements/flash.html')

    def _save_config(self):
        result = self.presenter.save_config()
        if result:
            flash(u'Configuration save', 'success')
        else:
            flash(u'Configuration not save', 'danger')
        return redirect(url_for('package', name=self.presenter.package_name))

    def _save_native(self):
        result = self.presenter.save_native()
        if result:
            flash(u'NAtive configuration save', 'success')
        else:
            flash(u'Native Configuration not save', 'danger')
        return redirect(url_for('package', name=self.presenter.package_name))
