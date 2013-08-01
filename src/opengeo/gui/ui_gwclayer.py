# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Thu Jul 25 11:46:11 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_EditGwcLayerDialog(object):
    def setupUi(self, EditGwcLayerDialog):
        EditGwcLayerDialog.setObjectName(_fromUtf8("EditGwcLayerDialog"))
        EditGwcLayerDialog.resize(528, 276)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EditGwcLayerDialog.sizePolicy().hasHeightForWidth())
        EditGwcLayerDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(EditGwcLayerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.layerLabel = QtGui.QLabel("Layer")
        self.horizontalLayout.addWidget(self.layerLabel)
        self.layerBox = QtGui.QComboBox()
        self.horizontalLayout.addWidget(self.layerBox)
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.groupBox = QtGui.QGroupBox(EditGwcLayerDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelWidth = QtGui.QLabel(self.groupBox)
        self.labelWidth.setObjectName(_fromUtf8("labelWidth"))
        self.horizontalLayout_3.addWidget(self.labelWidth)
        self.spinBoxWidth = QtGui.QSpinBox(self.groupBox)
        self.spinBoxWidth.setObjectName(_fromUtf8("spinBoxWidth"))
        self.horizontalLayout_3.addWidget(self.spinBoxWidth)
        self.labelHeight = QtGui.QLabel(self.groupBox)
        self.labelHeight.setObjectName(_fromUtf8("labelHeight"))
        self.horizontalLayout_3.addWidget(self.labelHeight)
        self.spinBoxHeight = QtGui.QSpinBox(self.groupBox)
        self.spinBoxHeight.setObjectName(_fromUtf8("spinBoxHeight"))
        self.horizontalLayout_3.addWidget(self.spinBoxHeight)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBoxFormats = QtGui.QGroupBox(EditGwcLayerDialog)
        self.groupBoxFormats.setObjectName(_fromUtf8("groupBoxFormats"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBoxFormats)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBoxPng = QtGui.QCheckBox(self.groupBoxFormats)
        self.checkBoxPng.setObjectName(_fromUtf8("checkBoxPng"))
        self.verticalLayout_2.addWidget(self.checkBoxPng)
        self.checkBoxPng8 = QtGui.QCheckBox(self.groupBoxFormats)
        self.checkBoxPng8.setObjectName(_fromUtf8("checkBoxPng8"))
        self.verticalLayout_2.addWidget(self.checkBoxPng8)
        self.checkBoxJpg = QtGui.QCheckBox(self.groupBoxFormats)
        self.checkBoxJpg.setObjectName(_fromUtf8("checkBoxJpg"))
        self.verticalLayout_2.addWidget(self.checkBoxJpg)
        self.checkBoxGif = QtGui.QCheckBox(self.groupBoxFormats)
        self.checkBoxGif.setObjectName(_fromUtf8("checkBoxGif"))
        self.verticalLayout_2.addWidget(self.checkBoxGif)
        self.horizontalLayout.addWidget(self.groupBoxFormats)
        self.groupBoxGridsets = QtGui.QGroupBox(EditGwcLayerDialog)
        self.groupBoxGridsets.setObjectName(_fromUtf8("groupBoxGridsets"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBoxGridsets)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.checkBox4326 = QtGui.QCheckBox(self.groupBoxGridsets)
        self.checkBox4326.setObjectName(_fromUtf8("checkBox4326"))
        self.verticalLayout_3.addWidget(self.checkBox4326)
        self.checkBox900913 = QtGui.QCheckBox(self.groupBoxGridsets)
        self.checkBox900913.setObjectName(_fromUtf8("checkBox900913"))
        self.verticalLayout_3.addWidget(self.checkBox900913)
        self.checkBoxGoogle = QtGui.QCheckBox(self.groupBoxGridsets)
        self.checkBoxGoogle.setObjectName(_fromUtf8("checkBoxGoogle"))
        self.verticalLayout_3.addWidget(self.checkBoxGoogle)
        self.checkBoxGlobalScale = QtGui.QCheckBox(self.groupBoxGridsets)
        self.checkBoxGlobalScale.setObjectName(_fromUtf8("checkBoxGlobalScale"))
        self.verticalLayout_3.addWidget(self.checkBoxGlobalScale)
        self.checkBoxGlobalPixel = QtGui.QCheckBox(self.groupBoxGridsets)
        self.checkBoxGlobalPixel.setObjectName(_fromUtf8("checkBoxGlobalPixel"))
        self.verticalLayout_3.addWidget(self.checkBoxGlobalPixel)
        self.horizontalLayout.addWidget(self.groupBoxGridsets)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(EditGwcLayerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EditGwcLayerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditGwcLayerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditGwcLayerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditGwcLayerDialog)

    def retranslateUi(self, EditGwcLayerDialog):
        EditGwcLayerDialog.setWindowTitle(_translate("EditGwcLayerDialog", "Dialog", None))
        self.groupBox.setTitle(_translate("EditGwcLayerDialog", "Metatiling factors", None))
        self.labelWidth.setText(_translate("EditGwcLayerDialog", "Width", None))
        self.labelHeight.setText(_translate("EditGwcLayerDialog", "Height", None))
        self.groupBoxFormats.setTitle(_translate("EditGwcLayerDialog", "Tile image formats", None))
        self.checkBoxPng.setText(_translate("EditGwcLayerDialog", "png", None))
        self.checkBoxPng8.setText(_translate("EditGwcLayerDialog", "png8", None))
        self.checkBoxJpg.setText(_translate("EditGwcLayerDialog", "jpg", None))
        self.checkBoxGif.setText(_translate("EditGwcLayerDialog", "gif", None))
        self.groupBoxGridsets.setTitle(_translate("EditGwcLayerDialog", "Gridsets", None))
        self.checkBox4326.setText(_translate("EditGwcLayerDialog", "EPSG:4326", None))
        self.checkBox900913.setText(_translate("EditGwcLayerDialog", "ESPG:900913", None))
        self.checkBoxGoogle.setText(_translate("EditGwcLayerDialog", "GoogleCRS84Quad", None))
        self.checkBoxGlobalScale.setText(_translate("EditGwcLayerDialog", "GlobalCRS84Scale", None))
        self.checkBoxGlobalPixel.setText(_translate("EditGwcLayerDialog", "GlobalCRS84Pixel", None))

