from flask import Flask
from flask_socketio import SocketIO
from src.Presenter.main_presenter import MainPresenter
from src.View.FreeconfFlask.main_view import MainView
from src.View.FreeconfFlask.package_view import PackageView

__author__ = 'Ondřej Lanč'


class FreeconfFlask(object):
    """View class for Freeconf. Have as property Flask and SocketiIO object.
    :param debug: bool
    """
    _flask = Flask(__name__)
    _socketio = SocketIO(_flask)
    def __init__(self, debug=False):
        self._presenter = MainPresenter()
        self._flask.debug = debug
        self._flask.config['SECRET_KEY'] = '56asdasss545'
        self._flask.config['TEMPLATES_AUTO_RELOAD'] = True
        # main view
        self._mainView = MainView(self._flask, self._socketio)
        # view for package
        self._packageView = PackageView(self._flask, self._socketio)

    def run(self):
        """main method for run server from Flask and SocketIO"""
        self._socketio.run(self._flask)
