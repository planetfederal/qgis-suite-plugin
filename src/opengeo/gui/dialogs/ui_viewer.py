# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_viewer.ui'
#
# Created: Mon Jul 21 14:30:21 2014
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_MetatoolsViewer(object):
    def setupUi(self, MetatoolsViewer):
        MetatoolsViewer.setObjectName(_fromUtf8("MetatoolsViewer"))
        MetatoolsViewer.resize(550, 350)
        MetatoolsViewer.setMinimumSize(QtCore.QSize(200, 100))
        MetatoolsViewer.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(MetatoolsViewer)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(MetatoolsViewer)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.webView = QtWebKit.QWebView(self.frame)
        self.webView.setMinimumSize(QtCore.QSize(250, 150))
        self.webView.setStyleSheet(_fromUtf8(""))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout_2.addWidget(self.webView)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsViewer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.actionPrint = QtGui.QAction(MetatoolsViewer)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/metatools/icons/menu_print.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionCopyAll = QtGui.QAction(MetatoolsViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/metatools/icons/menu_copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopyAll.setIcon(icon1)
        self.actionCopyAll.setObjectName(_fromUtf8("actionCopyAll"))
        self.actionCopy = QtGui.QAction(MetatoolsViewer)
        self.actionCopy.setIcon(icon1)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))

        self.retranslateUi(MetatoolsViewer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetatoolsViewer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetatoolsViewer.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsViewer)

    def retranslateUi(self, MetatoolsViewer):
        MetatoolsViewer.setWindowTitle(_translate("MetatoolsViewer", "Metadata viewer", None))
        self.actionPrint.setText(_translate("MetatoolsViewer", "Print", None))
        self.actionPrint.setShortcut(_translate("MetatoolsViewer", "Ctrl+P", None))
        self.actionCopyAll.setText(_translate("MetatoolsViewer", "Copy all", None))
        self.actionCopy.setText(_translate("MetatoolsViewer", "Copy", None))
        self.actionCopy.setShortcut(_translate("MetatoolsViewer", "Ctrl+C", None))

from PyQt4 import QtWebKit
import resources_rc
