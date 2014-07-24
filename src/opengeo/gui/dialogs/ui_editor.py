# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_editor.ui'
#
# Created: Wed Jul 23 16:18:43 2014
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

class Ui_MetatoolsEditor(object):
    def setupUi(self, MetatoolsEditor):
        MetatoolsEditor.setObjectName(_fromUtf8("MetatoolsEditor"))
        MetatoolsEditor.resize(1017, 782)
        MetatoolsEditor.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtGui.QVBoxLayout(MetatoolsEditor)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(MetatoolsEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.tab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.filterBox = QtGui.QLineEdit(self.widget)
        self.filterBox.setObjectName(_fromUtf8("filterBox"))
        self.horizontalLayout.addWidget(self.filterBox)
        self.buttonExpand = QtGui.QToolButton(self.widget)
        self.buttonExpand.setObjectName(_fromUtf8("buttonExpand"))
        self.horizontalLayout.addWidget(self.buttonExpand)
        self.buttonCollapse = QtGui.QToolButton(self.widget)
        self.buttonCollapse.setObjectName(_fromUtf8("buttonCollapse"))
        self.horizontalLayout.addWidget(self.buttonCollapse)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.treeFull = QtGui.QTreeWidget(self.widget)
        self.treeFull.setHeaderHidden(True)
        self.treeFull.setObjectName(_fromUtf8("treeFull"))
        self.treeFull.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_2.addWidget(self.treeFull)
        self.checkHighlight = QtGui.QCheckBox(self.widget)
        self.checkHighlight.setObjectName(_fromUtf8("checkHighlight"))
        self.verticalLayout_2.addWidget(self.checkHighlight)
        self.groupBox = QtGui.QGroupBox(self.splitter)
        self.groupBox.setEnabled(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lblNodePath = QtGui.QLabel(self.groupBox)
        self.lblNodePath.setWordWrap(True)
        self.lblNodePath.setObjectName(_fromUtf8("lblNodePath"))
        self.verticalLayout_4.addWidget(self.lblNodePath)
        self.textValue = QtGui.QTextEdit(self.groupBox)
        self.textValue.setObjectName(_fromUtf8("textValue"))
        self.verticalLayout_4.addWidget(self.textValue)
        self.verticalLayout.addWidget(self.splitter)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.webView = QtWebKit.QWebView(self.tab_2)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout_5.addWidget(self.webView)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.autoFillButton = QtGui.QPushButton(MetatoolsEditor)
        self.autoFillButton.setObjectName(_fromUtf8("autoFillButton"))
        self.horizontalLayout_2.addWidget(self.autoFillButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(MetatoolsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.actionCopyPath = QtGui.QAction(MetatoolsEditor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/metatools/icons/menu_copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopyPath.setIcon(icon)
        self.actionCopyPath.setObjectName(_fromUtf8("actionCopyPath"))

        self.retranslateUi(MetatoolsEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetatoolsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetatoolsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(MetatoolsEditor)

    def retranslateUi(self, MetatoolsEditor):
        MetatoolsEditor.setWindowTitle(_translate("MetatoolsEditor", "Metadata editor", None))
        self.buttonExpand.setText(_translate("MetatoolsEditor", "...", None))
        self.buttonCollapse.setText(_translate("MetatoolsEditor", "...", None))
        self.checkHighlight.setText(_translate("MetatoolsEditor", "Highlight empty fields", None))
        self.groupBox.setTitle(_translate("MetatoolsEditor", "Edit value", None))
        self.lblNodePath.setText(_translate("MetatoolsEditor", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MetatoolsEditor", "Edit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MetatoolsEditor", "View", None))
        self.autoFillButton.setText(_translate("MetatoolsEditor", "Fill from layer data", None))
        self.actionCopyPath.setText(_translate("MetatoolsEditor", "Copy path", None))
        self.actionCopyPath.setToolTip(_translate("MetatoolsEditor", "Copy node path to clipboard", None))

from PyQt4 import QtWebKit
