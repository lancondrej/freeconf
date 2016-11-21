#!/usr/bin/python3


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit
from flask_debugtoolbar import DebugToolbarExtension
from src.Presenter.main_presenter import MainPresenter
from src.View.Flask.main_view import MainView
from src.View.Flask.base_view import BaseView
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
        # self._flask.register_blueprint(package_blueprint)

        DebugToolbarExtension(self._flask)

        self._mainView=MainView(self._flask, self._socketio)
        self._packageView=PackageView(self._flask, self._socketio)
        # self._flask.config['DEBUG_TB_PROFILER_ENABLED'] = True

        # self._flask.add_url_rule('/', 'index', self.index)
        # self._flask.add_url_rule('/about', 'about', self.about)
        # self._flask.add_url_rule('/setting', 'setting', self.setting)
        # self._flask.add_url_rule('/<package_name>', 'package', self.package)
        #
        # self._flask.add_url_rule('/<package_name>/<tab_name>', 'tab', self.tab)
        # self._flask.add_url_rule('/_multiple_modal', 'multiple_modal', self.multiple_modal)
        # self._flask.add_url_rule('/_multiple_collapse', 'multiple_collapse', self.multiple_collapse)
        # self._flask.add_url_rule('/configure', 'configure', self.configure)
        #
        # self._socketio.on_event('submit', self.submit, namespace='/freeconf')
        # self._socketio.on_event('undo', self.undo, namespace='/freeconf')
        # self._socketio.on_event('redo', self.redo, namespace='/freeconf')
        # self._socketio.on_event('multiple_new', self.multiple_new, namespace='/freeconf')
        # self._socketio.on_event('multiple_delete', self.multiple_delete, namespace='/freeconf')
        # self._socketio.on_event('multiple_up', self.multiple_up, namespace='/freeconf')
        # self._socketio.on_event('multiple_down', self.multiple_down, namespace='/freeconf')
        # self._socketio.on_event('save_config', self.save_config, namespace='/freeconf')
        # self._socketio.on_event('save_native', self.save_native, namespace='/freeconf')

    # @property
    # def presenter(self):
    #     return self._presenter
    #
    # @presenter.setter
    # def presenter(self, presenter):
    #     self._presenter=presenter
    #
    # def setting(self):
    #     return self.package("Freeconf")
    #
    # def about(self):
    #     self._flask.update_template_context({'body': render_template("about.html")})
    #     return render_template('index.html')
    #     # return self.render_default(body= render_template("about.html"))
    #
    # def configure(self):
    #     packages=self.presenter.config.packages_list
    #     return self.render_default(body= render_template("configure.html", packages=packages))
    #
    # def render_default(self, tabs=None, body=""):
    #     return render_template('index.html', package_name=session.get('package_name'), tabs=tabs, main=body)

    # def package(self, package_name):
    #     if self.presenter.load_package(package_name):
    #         session['package_name']=package_name
    #         return self.render_default(tabs=self.presenter.package.tabs())
    #     else:
    #         return "error"
    # #
    # def submit(self):
    #     full_name = request.args.get('full_name')
    #     value = request.args.get('value')
    #     self.presenter.entry.save_value(full_name, value)
    #     return jsonify(result=value)
    #
    # def tab(self, package_name, tab_name):
    #     if package_name != session['package_name']:
    #         self.package(package_name)
    #     sections = self.presenter.package.tab(tab_name)
    #     Rsection = ""
    #     for section in sections:
    #         Rsection = Rsection + self._renderer.entry_render(section)
    #     return self.render_default(tabs = self.presenter.package.tabs(), body = Rsection)
    #
    # def index(self):
    #     return self.render_default()

    # def multiple_modal(self):
    #     full_name = request.args.get('full_name')
    #     entry = self.presenter.entry.get_entry(full_name)
    #     return self._renderer.render_modal(entry)
    #
    # def multiple_collapse(self):
    #     full_name = request.args.get('full_name')
    #     entry = self.presenter.entry.get_entry(full_name)
    #     return self._renderer.render_collapse(entry)
    #
    # def reload_element(self, full_name):
    #     entry = self.presenter.entry.get_entry(full_name)
    #     return self._renderer.reload_element(entry)
    #
    # def submit(self, data):
    #     full_name = data['full_name']
    #     value = data['value']
    #     self.presenter.entry.save_value(full_name, value)
    #     self.log("value change for {}".format(full_name))
    #
    def run(self):
        self._socketio.run(self._flask)

    # # def connect():
    # #     """Sent by clients when they enter a room.
    # #     A status message is broadcast to all people in the room."""
    # #     package = session.get('package')
    # #     # join_room(room)
    # #     emit('my_response', {'count': package})
    #
    # def multiple_new(self, data):
    #     full_name = data['full_name']
    #     result = self.presenter.entry.multiple_new(full_name)
    #     if result is None:
    #         self.flash_message("Cannot add element. Maximum element reach!", 'error')
    #     else:
    #         self.log("added entry for {}".format(full_name))
    #         emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #
    # def multiple_delete(self, data):
    #     full_name = data['full_name']
    #     value = data['value']
    #     result = self.presenter.entry.multiple_delete(full_name, value)
    #     if result is None:
    #         self.flash_message("Cannot remove element. Minimum element reach!", 'error')
    #     else:
    #         self.log("delete entry for {}".format(full_name))
    #         emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #
    # def multiple_up(self, data):
    #     full_name = data['full_name']
    #     value = data['value']
    #     self.presenter.entry.multiple_up(full_name, value)
    #     emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #     self.log("entry move up")
    #
    # def multiple_down(self, data):
    #     full_name = data['full_name']
    #     value = data['value']
    #     self.presenter.entry.multiple_down(full_name, value)
    #     emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #     self.log("entry move down")
    #
    # def undo(self):
    #     full_name = self.presenter.package.undo.undo()
    #     emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #     self.log("undo entry {}".format(full_name))
    #
    # def redo(self):
    #     full_name = self.presenter.package.undo.redo()
    #     emit('reload', {'full_name': full_name, 'rendered_entry': self.reload_element(full_name)}, namespace='/freeconf')
    #     self.log("redo entry {}".format(full_name))
    #
    # def flash_message(self, message, category):
    #     flash = render_template('elements/flash.html', category=category, message=message)
    #     emit('flash', {'flash': flash},  namespace='/freeconf')
    #
    # def log(self, message):
    #     emit('log', {'log_record': message},  namespace='/freeconf')
    #
    # def save_config(self):
    #     result = self.presenter.package.save_config()
    #     if result:
    #         self.flash_message('Configuration save', 'success')
    #     else:
    #         self.flash_message('Configuration not save', 'danger')
    #
    # def save_native(self):
    #     result = self.presenter.package.save_native()
    #     if result:
    #         self.flash_message('Native configuration save', 'success')
    #     else:
    #         self.flash_message('Native Configuration not save', 'danger')