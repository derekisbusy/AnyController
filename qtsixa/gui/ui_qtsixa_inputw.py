# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qtsixa_inputw.ui'
#
# Created: Wed Apr 20 03:13:23 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_InputDockWidget(object):
    def setupUi(self, InputDockWidget):
        InputDockWidget.setObjectName(_fromUtf8("InputDockWidget"))
        InputDockWidget.resize(476, 460)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        InputDockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(InputDockWidget)
        QtCore.QMetaObject.connectSlotsByName(InputDockWidget)

    def retranslateUi(self, InputDockWidget):
        InputDockWidget.setWindowTitle(_translate("InputDockWidget", "DockWidget", None))

