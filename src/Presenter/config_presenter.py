from src.Model.Config.freeconf_config import Config

__author__ = 'Ondřej Lanč'


class ConfigPresenter(object):
    def __init__(self):
        self._config = Config()

    @property
    def packages(self):
        return self._config.packages

    def package(self, name):
        return self._config.package(name)