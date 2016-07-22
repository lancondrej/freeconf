#!/usr/bin/python3
#
from IO.Input.XMLPackageParser.parser import XMLParser
from Model.package import PackageBase

__author__ = 'Ondřej Lanč'

input_parser = XMLParser("/home/ondra/škola/Freeconf/Freeconf/packages/test")
package = PackageBase("pokus")
input_parser.package=package
package.current_language = "en"
input_parser.load_package()
input_parser.load_plugins()
print("konec")
