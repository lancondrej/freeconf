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

    def write_native(self, groups=None):
        if groups:
            for group in groups:
                if group in self._config.group:
                    self._write_group(group)
        else:
            for group in self._config.group:
                self._write_group(plugin)

    def _write_group(self, groups):
        config_file_writer = ConfigFileWriter(self._config, self._package)
        native_file_writer = NativeFileWriter(self._native, self._xslt, config_file_writer)
        native_file_writer.write_native()
