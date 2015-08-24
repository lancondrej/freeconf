#!/usr/bin/python3

__author__ = 'Ondřej Lanč'

import os
import json
from Model.exception_logging.log import log
from Model.package import PackageBase

def get_env(var):
    """Get environment variable."""
    try:
        return os.environ[var]
    except KeyError:
        log.warning(
            'Unable to get the value of ' + var +
            ' environment variable!'
        )
        return None


class FreeconfModel(object):
    """Base class for Freeconf Model structure."""

    def __init__(self):
        self._freeconf_dirs = []
        self._homeDir = get_env('HOME')
        self._languages = []
        self._package = None

    @property
    def package(self):
        return self._package;

    @package.setter
    def package(self, package):
        assert isinstance(package, PackageBase)
        self._package = package

    @property
    def freeconf_dirs(self):
        return self._freeconf_dirs

    @freeconf_dirs.setter
    def freeconf_dirs(self, dirs):
        self._freeconf_dirs = dirs

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, langs):
        self._languages = langs

    def load_config(self, config_file=None):
        dirs = [
            self._homeDir + '/.freeconf',
            '/usr/local/share/freeconf',
            '/usr/share/freeconf'  # 'D:\Skola\workspace\FreeConf'
        ]
        langs = ['en', 'cs']
        config_data = [dirs, langs]
        if config_file is None:
            config_file=os.path.join(os.path.dirname(__file__), 'config/default.json')

        with open(config_file, mode='w', encoding='utf-8') as f:
            json.dump(config_data, f)

