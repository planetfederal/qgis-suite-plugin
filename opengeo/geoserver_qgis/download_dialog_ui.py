# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_dialog_ui.ui'
#
# Created: Mon Mar  4 18:25:03 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        DownloadDialog.setObjectName(_fromUtf8("DownloadDialog"))
        DownloadDialog.resize(771, 537)
        self.gridLayout_2 = QtGui.QGridLayout(DownloadDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_4 = QtGui.QLabel(DownloadDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.layerTreeView = QtGui.QTableView(DownloadDialog)
        self.layerTreeView.setObjectName(_fromUtf8("layerTreeView"))
        self.verticalLayout_2.addWidget(self.layerTreeView)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pbnDownload = QtGui.QPushButton(DownloadDialog)
        self.pbnDownload.setObjectName(_fromUtf8("pbnDownload"))
        self.horizontalLayout_3.addWidget(self.pbnDownload)
        self.pbnDownloadAdd = QtGui.QPushButton(DownloadDialog)
        self.pbnDownloadAdd.setObjectName(_fromUtf8("pbnDownloadAdd"))
        self.horizontalLayout_3.addWidget(self.pbnDownloadAdd)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.leServerUrl = QtGui.QLineEdit(DownloadDialog)
        self.leServerUrl.setMaxLength(32773)
        self.leServerUrl.setObjectName(_fromUtf8("leServerUrl"))
        self.gridLayout.addWidget(self.leServerUrl, 0, 1, 1, 1)
        self.pbnConnect = QtGui.QPushButton(DownloadDialog)
        self.pbnConnect.setObjectName(_fromUtf8("pbnConnect"))
        self.gridLayout.addWidget(self.pbnConnect, 3, 1, 1, 1)
        self.leUsername = QtGui.QLineEdit(DownloadDialog)
        self.leUsername.setObjectName(_fromUtf8("leUsername"))
        self.gridLayout.addWidget(self.leUsername, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(DownloadDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(DownloadDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(DownloadDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lePassword = QtGui.QLineEdit(DownloadDialog)
        self.lePassword.setObjectName(_fromUtf8("lePassword"))
        self.gridLayout.addWidget(self.lePassword, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(QtGui.QApplication.translate("DownloadDialog", "GeoServer Bridge - Download layers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DownloadDialog", "Layers available on the server:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownload.setText(QtGui.QApplication.translate("DownloadDialog", "Download the selected layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownloadAdd.setText(QtGui.QApplication.translate("DownloadDialog", "Download and add the selected layers to QGIS ", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnConnect.setText(QtGui.QApplication.translate("DownloadDialog", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DownloadDialog", "Username :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DownloadDialog", " Password  :", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DownloadDialog", "Server URL :", None, QtGui.QApplication.UnicodeUTF8))

