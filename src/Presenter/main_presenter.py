from flask_debugtoolbar import DebugToolbarExtension

from src.Presenter.config_presenter import ConfigPresenter
from src.Presenter.package_presenter import PackagePresenter
from src.View.Flask.freeconf_flask import FreeconfFlask
from src.Presenter.presenter import Presenter

__author__ = 'Ondřej Lanč'


class MainPresenter(Presenter):
    def __init__(self):
        self._config=ConfigPresenter()
        self._package=None
        self._view=None


    def enable_view(self):
        app = FreeconfFlask(__name__)
        app.config.from_object(__name__)
        app.jinja_env.autoescape = False
        app.secret_key = 'some_secret'
        app.debug = True
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        toolbar = DebugToolbarExtension(app)
        return app


    @property
    def package(self):
        return self._package

    @property
    def config(self):
        return self._config

    def load_package(self, name):
        if self.package is not None and self.package.package_name == name:
            return True
        if name not in self.config.packages_list:
            return False
        self._package=PackagePresenter(self.config.package(name))
        self.package.load_package()
        return True

    @property
    def entry(self):
        return self.package.entry