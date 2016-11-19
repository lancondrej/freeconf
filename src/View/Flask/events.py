from flask import session, render_template
from flask_socketio import emit, join_room, leave_room
from src.View.Flask.main import socketio

__author__ = 'Ondřej Lanč'

from src.View.Flask.routes import presenter, freeconf_flask

@socketio.on('connect', namespace='/freeconf')
def connect():
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    package = session.get('package')
    # join_room(room)
    emit('my_response', {'count': package})


@socketio.on('submit', namespace='/freeconf')
def submit(data):
    full_name = data['full_name']
    value = data['value']
    presenter.entry.save_value(full_name, value)
    log("value change for {}".format(full_name))


@socketio.on('multiple_new', namespace='/freeconf')
def multiple_new(data):
    full_name = data['full_name']
    result = presenter.entry.multiple_new(full_name)
    if result is None:
        flash_message("Cannot add element. Maximum element reach!", 'error')
    else:
        log("added entry for {}".format(full_name))
        emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')


@socketio.on('multiple_delete', namespace='/freeconf')
def multiple_delete(data):
    full_name = data['full_name']
    value = data['value']
    result = presenter.entry.multiple_delete(full_name, value)
    if result is None:
        flash_message("Cannot remove element. Minimum element reach!", 'error')
    else:
        log("delete entry for {}".format(full_name))
        emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')


@socketio.on('multiple_up', namespace='/freeconf')
def multiple_up(data):
    full_name = data['full_name']
    value = data['value']
    presenter.entry.multiple_up(full_name, value)
    emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')
    log("entry move up")


@socketio.on('multiple_down', namespace='/freeconf')
def multiple_down(data):
    full_name = data['full_name']
    value = data['value']
    presenter.entry.multiple_down(full_name, value)
    emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')
    log("entry move down")


@socketio.on('undo', namespace='/freeconf')
def undo():
    full_name = presenter.package.undo.undo()
    emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')
    log("undo entry {}".format(full_name))


@socketio.on('redo', namespace='/freeconf')
def redo():
    full_name = presenter.package.undo.redo()
    emit('reload', {'full_name': full_name, 'rendered_entry': freeconf_flask.reload_element(full_name)}, namespace='/freeconf')
    log("redo entry {}".format(full_name))


def flash_message(message, category):
    flash = render_template('elements/flash.html', category=category, message=message)
    emit('flash', {'flash': flash},  namespace='/freeconf')


def log(message):
    emit('log', {'log_record': message},  namespace='/freeconf')


@socketio.on('save_config', namespace='/freeconf')
def save_config():
    result = presenter.package.save_config()
    if result:
        flash_message('Configuration save', 'success')
    else:
        flash_message('Configuration not save', 'danger')


@socketio.on('save_native', namespace='/freeconf')
def save_native():
    result = presenter.package.save_native()
    if result:
        flash_message('Native configuration save', 'success')
    else:
        flash_message('Native Configuration not save', 'danger')
