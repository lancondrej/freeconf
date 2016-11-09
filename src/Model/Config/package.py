import os

__author__ = 'Ondřej Lanč'

class Package(object):
    def __init__(self):
        self.name = ""
        self.location = ""
        self.file = self.Files()
        self._groups = {}
        self.available_language = ["en", "cs"]

    def add_group(self, group):
        self._groups[group.name]=group

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

    @property
    def help_file(self):
        return os.path.join(self.location, self.file.help) if self.file.help else None

    @property
    def gui_label_file(self):
        return os.path.join(self.location, self.file.gui_label) if self.file.gui_label else None

    @property
    def default_values_file(self):
        return os.path.join(self.location, self.file.default_values) if self.file.default_values else None

    @property
    def output_file(self):
        return os.path.join(self.location, self.file.output) if self.file.output else None

    @property
    def _lists_dir(self):
        return os.path.join(self.location, 'lists')

    @property
    def _plugins_dir(self):
        return os.path.join(self.location, 'plugins')


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