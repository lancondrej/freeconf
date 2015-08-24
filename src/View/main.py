#!/usr/bin/python3
#

from PyQt4 import QtGui
from View.renderer import GuiHandler
from Controller.client_interface import PackageInterface
import sys

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("No package name was given.")
        exit(2)

    app = QtGui.QApplication(sys.argv)
    package = PackageInterface()
    package.load_package(sys.argv[1])
    # try:
    # p.loadPackage()
    # except:
        # print "Freeconf library init failed!"
        # exit(-1)

    widget = GuiHandler(package)
    widget.show()
    app.exec_()
    pass