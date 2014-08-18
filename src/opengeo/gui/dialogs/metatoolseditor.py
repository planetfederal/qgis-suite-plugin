# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011 BV (enickulin@bv.com)
# Copyright (C) 2011 NextGIS (info@nextgis.ru)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

import os
import sys
import dateutil.parser

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns import QXmlQuery

from qgis.core import *
from qgis.gui import *

from opengeo import config
from opengeo.metadata.dom_model import DomModel, FilterDomModel
from opengeo.metadata.tools import *
from opengeo.metadata.metadata_provider import MetadataProvider
from opengeo.metadata.standards import *
from ui_editor import Ui_MetatoolsEditor


class MetatoolsEditor(QMainWindow, Ui_MetatoolsEditor):
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint)
        self.lblNodePath.setText("")
        self.numberValue.setValidator(QDoubleValidator(self))
        self.lblNodePath.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.lblNodePath.addAction(self.actionCopyPath)
        self.connect(self.actionCopyPath, SIGNAL("activated()"), self.slotCopyPath)
        self.actionSave.triggered.connect(self.saveMetadata)
        self.actionValidate.triggered.connect(self.validate)
        self.actionClose.triggered.connect(self._closeWindow)
        self.actionImport.triggered.connect(self.importFromFile)
        self.actionNew.triggered.connect(self.createIso)
        self.actionFillFromLayer.triggered.connect(self.autofill)
        self.actionShowOptional.toggled.connect(self.updateDisplay)
        self.actionShowConditional.toggled.connect(self.updateDisplay)
        self.actionHighlightEmpty.toggled.connect(self.updateDisplay)
        self.treeFull.itemClicked.connect(self.itemSelected)
        self.textValue.textChanged.connect(self.valueModified)
        self.comboValue.currentIndexChanged.connect(self.valueModified)
        self.numberValue.textChanged.connect(self.valueModified)
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.filterBox.textChanged.connect(self.updateDisplay)
        self.buttonCollapse.clicked.connect(self.collapse)
        self.buttonExpand.clicked.connect(self.expand)

        self.textValue.setVisible(False)
        self.comboValue.setVisible(True)
        self.dateValue.setVisible(False)
        self.numberValue.setVisible(False)

        self.lastValueItem = None
        self.hasChanged = False


    def autofill(self):
        transform = QgsCoordinateTransform(self.layer.crs(), QgsCoordinateReferenceSystem("EPSG:4326"))
        layerExtent = transform.transform(self.layer.extent())

        xmin = layerExtent.xMinimum()
        xmax = layerExtent.xMaximum()
        ymin = layerExtent.yMinimum()
        ymax = layerExtent.yMaximum()

        self.metaProvider.setExtent(self.metaXML, (xmin, xmax, ymin, ymax))
        #self.metaProvider.setNumFeatures(self.layer.featureCount())
        self.updateTree()
        self.hasChanged = True
        QMessageBox.information(self, "Autofill metadata",
                                      "Metadata has been correctly completed using layer values.",
                                      QMessageBox.Ok)

        self.updateTree()

    def validate(self):
        if not self.metaProvider.checkExists():
            QMessageBox.information(self, "Validation", "No metadata to validate")
        try:
            self.metaProvider.validate()
            QMessageBox.information(self, "Validation", "Metadata correctly validated")
        except Exception, e:
            print e
            QMessageBox.warning(self, "Validation", "Metadata does not validate")

    def updateDisplay(self):
        text = self.filterBox.text().strip(' ').lower()
        self._updateItem(self.treeFull.invisibleRootItem(), text)
        if text:
            self.treeFull.expandAll()
        else:
            self.treeFull.collapseAll()
            self.treeFull.invisibleRootItem().child(0).setExpanded(True)

    def _updateItem(self, item, text):
        if (item.childCount() > 0):
            show = False
            for i in xrange(item.childCount()):
                child = item.child(i)
                showChild = self._updateItem(child, text)
                show = showChild or show
            item.setHidden(not show)
            return show
        elif isinstance(item, ValueItem):
            hide = bool(text) and (text not in item.text(0).lower())
            showOptional = self.actionShowOptional.isChecked()
            showConditional = self.actionShowConditional.isChecked()
            highlightEmpty = self.actionHighlightEmpty.isChecked()
            if item.obligation == OBLIGATION_OPTIONAL and not showOptional:
                hide = True
            if item.obligation == OBLIGATION_CONDITIONAL and not showConditional:
                hide = True
            item.highlight(highlightEmpty)
            item.setHidden(hide)
            return not hide
        else:
            item.setHidden(True)
            return False

    def expand(self):
        self.treeFull.expandAll()

    def collapse(self):
        self.treeFull.collapseAll()

    def slotCopyPath(self):
        QApplication.clipboard().setText(self.lblNodePath.text())

    def importFromFile(self):
        if self.askOverwrite():
            filename = QFileDialog.getOpenFileName(self,
                                       "Select metadata file",
                                       "",
                                       'XML files (*.xml);;Text files (*.txt *.TXT);;All files (*.*)'
                                      )
            if filename:
                try:
                    self.metaProvider.importFromFile(filename)
                    self.setContent(self.metaProvider, self.layer)
                except Exception, e:
                    QMessageBox.warning(self, "Import metadata", "Could not import metadata.\n" +
                                                unicode(e), QMessageBox.Ok)

    def askOverwrite(self):
        if not self.metaProvider.checkExists():
            return True
        ret = QMessageBox.warning(self, "Create metadata", "The layer already has metadata.\n"
                                        "Do you really want to overwrite the existing metadata?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return ret == QMessageBox.Yes

    def _createNew(self, std):
        if self.askOverwrite():
            try:
                template = std.getTemplate(self.layer)
                self.metaProvider.setMetadata(template)
                self.setContent(self.metaProvider, self.layer)
            except Exception, e:
                QMessageBox.warning(self, "Import metadata", "Could not import metadata.\n" +
                            unicode(e), QMessageBox.Ok)
    def createIso(self):
        self._createNew(IsoStandard())

    def setContent(self, metaProvider, layer):
        self.actionFillFromLayer.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.metaProvider = metaProvider
        self.layer = layer

        self.textValue.setVisible(False)
        self.numberValue.setVisible(False)
        self.comboValue.setVisible(False)
        self.dateValue.setVisible(False)
        self.labelWarning.setVisible(False)

        if not self.metaProvider.checkExists():
            return

        #self.metaProvider.validate()

        self.actionFillFromLayer.setEnabled(True)
        self.actionSave.setEnabled(True)

        self.metaXML = QDomDocument()
        metadata = self.metaProvider.getMetadata().encode("utf-8")
        self.metaXML.setContent(metadata)

        self.updateTree()

    def updateTree(self):
        self.treeFull.clear()
        root = self.metaXML.documentElement()
        n = root.firstChild()
        while not n.isNull():
            item = self._getItemForNode(n)
            n = n.nextSibling()
            if item is not None:
                self.treeFull.addTopLevelItem(item)
        self.lastValueItem = None
        self.labelWarning.setVisible(False)
        self.textValue.setVisible(False)
        self.numberValue.setVisible(False)
        self.comboValue.setVisible(False)
        self.dateValue.setVisible(False)
        self.groupBox.setEnabled(False)
        self.updateDisplay()

    def itemSelected(self, item, column):
        self.textValue.blockSignals(True)
        self.applyEdits()
        self.labelWarning.setVisible(False)
        self.textValue.setVisible(False)
        self.numberValue.setVisible(False)
        self.dateValue.setVisible(False)
        self.comboValue.setVisible(False)
        if isinstance(item, ValueItem):
            self.lastValueItem = item
            clist = codelist(item.scheme)
            if clist is not None:
                self.comboValue.clear()
                self.comboValue.addItems(clist)
                self.comboValue.setCurrentIndex(0)
                idx = self.comboValue.findText(item.value)
                if idx != -1:
                    self.comboValue.setCurrentIndex(idx)
                elif item.value is not None:
                    self.labelWarning.setText("The existing value is not a correct option: " + item.value)
                    self.labelWarning.setVisible(True)
                self.comboValue.setVisible(True)
            elif item.scheme.endswith("Date"):
                self.dateValue.setVisible(True)
                try:
                    date = dateutil.parser.parse(item.value)
                    self.dateValue.setSelectedDate(date)
                except:
                    if item.value is not None:
                        self.labelWarning.setText("The existing value is not a correct date: " + item.value)
                        self.labelWarning.setVisible(True)
            elif item.scheme.endswith("Decimal"):
                self.numberValue.setVisible(True)
                if item.value is not None:
                    self.numberValue.setText(item.value)
                else:
                    self.numberValue.setText("")
            else:
                if item.value is not None:
                    self.textValue.setPlainText(item.value)
                else:
                    self.textValue.setPlainText("")
                self.textValue.setVisible(True)


            self.groupBox.setEnabled(True)
        else:
            self.lastValueItem = None

            self.groupBox.setEnabled(False)
        self.textValue.blockSignals(False)
        path = getPath(item.node)
        self.lblNodePath.setText(path)

    def tabChanged(self, tab):
        if tab == 1:
            html = self.metaProvider.getHtml()
            if html:
                #QXmlPattern does not support CDATA section
                html = html.replace('&amp;', '&')
                html = html.replace('&gt;', '>')
                result = html.replace('&lt;', '<')

                self.webView.setHtml(result)

    def valueModified(self):
        self.hasChanged = True

    def applyEdits(self):
        if self.lastValueItem is not None:
            value = None
            if self.textValue.isVisible():
                value = self.textValue.toPlainText()
            elif self.comboValue.isVisible():
                value = self.comboValue.currentText()
            elif self.dateValue.isVisible():
                value = str(self.dateValue.selectedDate())
            elif self.numberValue.isVisible():
                value = str(self.numberValue.text())
            if value:
                self.lastValueItem.value = value
                node = self.lastValueItem.node
                if not node.hasChildNodes():
                    textNode = node.ownerDocument().createTextNode(value)
                    node.appendChild(textNode)
                else:
                    node.childNodes().at(0).setNodeValue(value)
                self.lastValueItem.highlight(True)


    def saveMetadata(self):
        try:
            self.metaProvider.setMetadata(unicode(self.metaXML.toString()))
            self.hasChanged = False
        except:
            QMessageBox.warning(self,
                                self.tr("Error saving metadata"),
                                self.tr("Metadata can't be saved:\n") + unicode(sys.exc_info()[0])
                             )


    def _closeWindow(self):
        if self.hasChanged:
            ret = QMessageBox.warning(self, "Close",
                                      "There are unsaved values. Do you want to close without saving?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.hide()

    def closeEvent(self, evt):
        if self.hasChanged:
            ret = QMessageBox.question(self,"Close",
                                       "There are unsaved changes. Do you want to close without saving?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if ret == QMessageBox.Yes:
                evt.accept()
            else:
                evt.ignore()
        else:
            evt.accept()

    def _getItemForNode(self, node):
        subnodes = node.childNodes()
        if subnodes.at(0).nodeType() == QDomNode.TextNode:
            return subnodes.at(0).toText().nodeValue(), node.nodeName()
        elif subnodes.isEmpty():
            clist = codelist(node.nodeName())
            if clist is not None or node.nodeName().startswith("gco"):
                return None, node.nodeName()
            return ValueItem(node, node.nodeName(), None, node.nodeName())
        else:
            item = NodeItem(node)
            for i in xrange(subnodes.length()):
                n = subnodes.at(i)
                ret = self._getItemForNode(n)
                if isinstance(ret, (NodeItem, ValueItem)):
                    item.addChild(ret)
                else:
                    child = ValueItem(n, node.nodeName(), ret[0], ret[1])
                    if subnodes.length() == 1:
                        return child
                    else:
                        item.addChild(child)
            return item


def getPath(node):
    path = ""
    if not node.parentNode().isNull() and node.parentNode().nodeType() != QDomNode.DocumentNode:
        path = getPath(node.parentNode()) + " -> "

    return path + node.nodeName()



class NodeItem(QTreeWidgetItem):
    def __init__(self, node):
        QTreeWidgetItem.__init__(self)
        self.node = node
        self.obligation = elementObligation(node.nodeName())
        self.setText(0, elementLabel(node.nodeName()))
        self.setIcon(0, self.obligationIcon())


    def obligationIcon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), os.pardir,
                                  os.pardir, "images", "%s.gif" % self.obligation))

class ValueItem(NodeItem):
    def __init__(self, node, name, value, scheme):
        QTreeWidgetItem.__init__(self)
        self.node = node
        self.name = name
        self.value = value
        self.scheme = scheme
        self.obligation = elementObligation(name)
        self.setText(0, elementLabel(name))
        self.setIcon(0, self.obligationIcon())

    def highlight(self, b):
        font = self.font(0);
        empty = self.value is None
        font.setBold(b and empty);
        self.setFont(0, font)


