#!/usr/bin/python3


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, emit
from src.View.Flask.renderer import Renderer
from flask.views import View

__author__ = 'Ondřej Lanč'


class BaseView(object):
    _renderer = Renderer()

    def __init__(self, flask, socketio):
        self._flask = flask
        self._socketio = socketio

    def render_default(self, tabs=None, body=""):
        return render_template('index.html', package_name=session.get('package_name'), tabs=tabs, main=body)

    def flash_message(self, message, category):
        flash = render_template('elements/flash.html', category=category, message=message)
        emit('flash', {'flash': flash},  namespace='/freeconf')

    def log(self, message):
        emit('log', {'log_record': message},  namespace='/freeconf')