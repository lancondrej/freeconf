#!/usr/bin/python3
#
from Model.package import PackageBase
from IO.Input.XMLPackageParser.parser import XMLParser

__author__ = 'Ondřej Lanč'

input_parser = XMLParser("/home/ondra/škola/Freeconf/new_freeconf/packages/apache")
package = PackageBase("pokus")
input_parser.package=package
package.current_language = "en"
input_parser.load_package()
input_parser.load_plugins()
print("konec")
