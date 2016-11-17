#!/usr/bin/python3


from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect, Namespace
from src.View.Flask.renderer import Renderer

__author__ = 'Ondřej Lanč'

thread = None


class FreeconfFlask(object):
    _flask = Flask(__name__)

    _flask.config.from_object(__name__)
    _flask.jinja_env.autoescape = False
    _flask.secret_key = 'some_secret'
    _flask.debug = True
    _flask.config['DEBUG_TB_PROFILER_ENABLED'] = True
    _flask.config['TEMPLATES_AUTO_RELOAD'] = True
    _flask.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    toolbar = DebugToolbarExtension(_flask)
    _socket_io = SocketIO(_flask)

    def __init__(self):
        self._presenter = None




        self._renderer = Renderer()
        self._flask.add_url_rule('/', 'index', self.index)
        self._flask.add_url_rule('/about', 'about', self.about)
        self._flask.add_url_rule('/setting', 'setting', self.setting)
        self._flask.add_url_rule('/package/<name>', 'package', self.package)
        self._flask.add_url_rule('/tab/<name>', 'tab', self.tab)

        self._flask.add_url_rule('/_multiple_new', 'multiple_new', self.multiple_new)
        self._flask.add_url_rule('/_multiple_delete', 'multiple_delete', self.multiple_delete)
        self._flask.add_url_rule('/_multiple_up', 'multiple_up', self.multiple_up)
        self._flask.add_url_rule('/_multiple_down', 'multiple_down', self.multiple_down)
        self._flask.add_url_rule('/_multiple_modal', 'multiple_modal', self.multiple_modal)
        self._flask.add_url_rule('/_multiple_collapse', 'multiple_collapse', self.multiple_collapse)

        self._flask.add_url_rule('/_reload_element', 'reload_element', self.reload_element)
        self._flask.add_url_rule('/_flash', 'flash_message', self.flash_message)
        self._flask.add_url_rule('/_submit', 'submit', self.submit)
        self._flask.add_url_rule('/configure', 'configure', self.configure)
        self._flask.add_url_rule('/_save_config', 'save_config', self._save_config)
        self._flask.add_url_rule('/_save_native', 'save_native', self._save_native)

        self._flask.add_url_rule('/_undo', 'undo', self._undo)
        self._flask.add_url_rule('/_redo', 'redo', self._redo)

        # self.app.add_url_rule('/users/', view_func=ShowUsers.as_view('show_users'))


    class MyNamespace(Namespace):

        def on_my_ping(self):
            emit('my_pong')

        def on_connect(self):
            global thread
            if thread is None:
                thread = FreeconfFlask._socket_io.start_background_task(target=FreeconfFlask.background_thread)
            emit('my_response', {'data': 'Connected', 'count': 0})

        def on_disconnect(self):
            print('Client disconnected', request.sid)

    _socket_io.on_namespace(MyNamespace('/test'))

    @classmethod
    def background_thread(cls):
        """Example of how to send server generated events to clients."""
        count = 0
        while True:
            cls._socket_io.sleep(0.1)
            count += 666
            cls._socket_io.emit('my_response',
                                {'data': 'Server generated event', 'count': count},
                                namespace='/test')

    def run(self, host=None, port=None, **options):
        self._socket_io.run(self._flask, host, port, **options)

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
