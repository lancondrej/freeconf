#!/usr/bin/python3
#
from src.IO.input import Input
from src.IO.exception_logging.log import log

__author__ = 'Ondřej Lanč'


class XMLParser(Input):
    def __init__(self, package, package_config):
        self.package = package
        self.package_config = package_config

    def load_package(self):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_config(self, source):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

    def load_packages_config(self):
        pass

    def load_header(self):
        log.info("Loading header file" + self.package_config.path)
        # header_file_parser = HeaderFileReader()
        # if self.package.is_plugin:
        #     header_file_parser.parse(self._paths.header_file_full_path, package)
        # else:
        #     header_file_parser.parse(self._paths.header_file_full_path)
        # header_structure = header_file_parser.headerStructure
        #
        # # Path to template file
        # self._paths.templateFile = header_structure.templateFile
        # self._paths.templateFile.fullPath = os.path.join(self._paths.main_dir, header_structure.templateFile.name)
        # # Path to dependencies file
        # if header_structure.dependenciesFile and header_structure.dependenciesFile.name is not None:
        #     self._paths.dependenciesFile = header_structure.dependenciesFile
        #     self._paths.dependenciesFile.fullPath = os.path.join(self._paths.main_dir,
        #                                                          header_structure.dependenciesFile.name)
        # # Path to gui template file
        # if header_structure.guiTemplateFile and header_structure.guiTemplateFile.name is not None:
        #     self._paths.guiTemplateFile = header_structure.guiTemplateFile
        #     self._paths.guiTemplateFile.fullPath = os.path.join(self._paths.main_dir,
        #                                                         header_structure.guiTemplateFile.name)
        # # Path to output file
        # if header_structure.outputFile and header_structure.outputFile.name is not None:
        #     self._paths.outputFile = header_structure.outputFile
        #     self._paths.outputFile.fullPath = self._expand_file_name(header_structure.outputFile.name)
        #
        # self._paths.helpFile = header_structure.helpFile
        # self._paths.guiLabelFile = header_structure.guiLabelFile
        # self._paths.defaultValuesFile = header_structure.defaultValuesFile
        #
        # # Process groups
        # for group in header_structure.groups.values():
        #     if group.native_output.name:
        #         group.native_output.fullPath = self._expand_file_name(group.native_output.name)
        #     if group.transform.name:
        #         group.transform.fullPath = os.path.join(self._paths.main_dir, group.transform.name)
        # for group in package.available_groups.values():
        #     for i in group.included_transforms:
        #         i.fullPath = os.path.join(self._paths.main_dir, i.name)
        # package.groups = header_structure.groups
        # # Create default group if there was no in the header file
        # if len(package.groups) == 0:
        #     log.warning("No group defined in header file. Creating default group.")
        #     group = FcGroup("default")
        #     package.groups[group.name] = group
        #
        # # Fill map of listFiles.
        # for f in header_structure.listFiles:
        #     # We do not know path to list file, so it is empty for now.
        #     self._paths.listFiles[f] = None

    def load_plugins(self, plugins=[]):
        """Virtual function. Need to be reimplemented in subclass"""
        raise NotImplementedError

