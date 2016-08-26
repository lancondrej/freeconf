#!/usr/bin/python3
#
from IO.Input.XMLPackageParser.parser import XMLParser
from IO.Output.XML.output import XMLOutput
from Model.package import PackageBase

__author__ = 'Ondřej Lanč'

input_parser = XMLParser("/home/ondra/škola/Freeconf/Freeconf/packages/apache")
package = PackageBase("pokus")
input_parser.package=package
package.current_language = "en"
input_parser.load_package()
input_parser.load_plugins()

output=XMLOutput(package)
output.write_output()

import lxml.etree as ET

dom = ET.parse('output.xml')
xslt = ET.parse('xslt.xsl')
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(str(newdom))
# print(ET.tostring(newdom, pretty_print=True))


print("konec")
