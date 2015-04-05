#!/usr/bin/python3
#
from Model.package import PackageBase
from IO.Input.XMLPackageParser.parser1 import XMLParser

__author__ = 'Ondřej Lanč'

input_parser = XMLParser("/home/ondra/škola/Freeconf/new_freeconf/packages/apache")
package = PackageBase("pokus")
package.input = input_parser
package.current_language = "en"
package.load_package()
print("konec")
