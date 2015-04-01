#!/usr/bin/python3
#
from Model.package import PackageBase
from IO.Input.XMLPackageParser.parser1 import XMLParser

__author__ = 'Ondřej Lanč'

input_parser = XMLParser("/home/ondra/škola/Freeconf/old_freeconf/packages/apache")
package = PackageBase("pokus")
package.input = input_parser
package.load_package(None)
print("konec")
