#!/usr/bin/python3
#
from src.IO.XMLParser.input import XMLParser
from src.Model.Package.package import Package
from src.Model.Config.package_config import PackageConfig
from src.Presenter.config_presenter import ConfigPresenter

__author__ = 'Ondřej Lanč'
package = Package("pokus")
package_config = PackageConfig()
input_parser = XMLParser(package,package_config)
input_parser.package=package

package.current_language = "en"


config=ConfigPresenter()

# input_parser.load_package()
# input_parser.load_plugins()
#
# output=XMLOutput(package)
# output.write_output()
#
# import lxml.etree as ET
#
# dom = ET.parse('output.xml')
# xslt = ET.parse('xslt.xsl')
# transform = ET.XSLT(xslt)
# newdom = transform(dom)
# print(str(newdom))
# # print(ET.tostring(newdom, pretty_print=True))
#

print("konec")
