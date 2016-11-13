from src.IO.XMLParser.config_file import ConfigFileWriter
from src.IO.XMLParser.native_file import NativeFileWriter
from src.IO.output import Output

__author__ = 'Ondřej Lanč'


class XMLOutput(Output):

    def __init__(self, config, package):
        self._config = config
        self._package = package

    def write_output(self):
        ConfigFileWriter(self._config, self._package).write_config()
        for plugin in self._package.plugins:
            ConfigFileWriter(self._config.plugin(plugin.name), plugin).write_config()

    def write_native(self, groups=None):
        if groups:
            for group in groups:
                if group in self._config.groups:
                    self._write_group(self._config.group(group))
        else:
            for group in self._config.groups.values():
                if group.output_defaults:
                    self._write_group(group)

    def _write_group(self, group):
        config_file_writer = ConfigFileWriter(self._config, self._package)
        NativeFileWriter(group, config_file_writer.get_config(group)).write_native()
