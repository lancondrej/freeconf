import os

__author__ = 'Ondřej Lanč'


class Package(object):
    def __init__(self):
        self.name = ""
        self.location = ""
        self.file = self.Files()
        self._groups = {}
        self.available_language = []
        self.default_language = None
        self._plugins = {}

    @property
    def header_file(self):
        return os.path.join(self.location, self.file.header) if self.file.header else None

    @property
    def list_file(self):
        return os.path.join(self._lists_dir, self.file.list) if self.file.list else None

    @property
    def template_file(self):
        return os.path.join(self.location, self.file.template) if self.file.template else None

    @property
    def dependencies_file(self):
        return os.path.join(self.location, self.file.dependencies) if self.file.dependencies else None

    @property
    def gui_template_file(self):
        return os.path.join(self.location, self.file.gui_template) if self.file.gui_template else None

    def help_file(self, language):
        if language not in self.available_language:
            language=self.default_language
        return os.path.join(self.languages_dir, language, self.file.help) if self.file.help else None

    def list_help_file(self, language):
        if language not in self.available_language:
            language=self.default_language
        return os.path.join(self._lists_dir, "L10n", language, self.file.list) if (self.file.list and language) else None

    def gui_help_file(self, language):
        if language not in self.available_language:
            language=self.default_language
        return os.path.join(self.languages_dir, language, self.file.gui_label) if (self.file.gui_label and language) else None

    @property
    def default_values_file(self):
        return os.path.join(self.location, self.file.default_values) if self.file.default_values else None

    @property
    def config_file(self):
        return os.path.join(self.location, self.file.output) if self.file.output else None

    @property
    def _lists_dir(self):
        return os.path.join(self.location, 'lists')

    @property
    def plugins_dir(self):
        return os.path.join(self.location, 'plugins')

    @property
    def languages_dir(self):
        return os.path.join(self.location, 'L10n')

    def group(self, name):
        return self._groups.get(name)

    def add_group(self, group):
        self._groups[group.name] = group

    def add_plugin(self, plugin):
        plugin.parent=self
        self._plugins[plugin.name]=plugin

    @property
    def plugins(self):
        return self._plugins

    def plugin(self, name):
        return self._plugins.get(name)


    class Files(object):
        def __init__(self):
            self.header = "header.xml"
            self.list = None
            self.template = None
            self.dependencies = None
            self.gui_template = None
            self.help = None
            self.gui_label = None
            self.default_values = None
            self.output = None


class Plugin(Package):
    def __init__(self):
        Package.__init__(self)
        self.parent=None