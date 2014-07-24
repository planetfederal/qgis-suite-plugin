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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns import QXmlQuery

from qgis.core import *
from qgis.gui import *

import sys
from opengeo.metadata.dom_model import DomModel, FilterDomModel
from opengeo.metadata.metadata_provider import MetaInfoStandard
from ui_editor import Ui_MetatoolsEditor

class MetatoolsEditor(QDialog, Ui_MetatoolsEditor):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint)

        self.lblNodePath.setText("")

        self.btnSave = self.buttonBox.button(QDialogButtonBox.Save)
        self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

        #contextmenu
        self.lblNodePath.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.lblNodePath.addAction(self.actionCopyPath)
        self.connect(self.actionCopyPath, SIGNAL("activated()"), self.slotCopyPath)

        self.treeFull.itemClicked.connect(self.itemSelected)

        self.textValue.textChanged.connect(self.valueModified)

        self.buttonBox.accepted.disconnect(self.accept)
        self.btnSave.clicked.connect(self.saveMetadata)

        self.tabWidget.currentChanged.connect(self.tabChanged)

        self.filterBox.textChanged.connect(self.filterChanged)
        self.buttonCollapse.clicked.connect(self.collapse)
        self.buttonExpand.clicked.connect(self.expand)
        self.autoFillButton.clicked.connect(self.autofill)
        self.checkHighlight.stateChanged.connect(self.highlightChanged)

        self.lastValueItem = None




    def autofill(self):
        pass

    def highlightChanged(self, state):
        if state == Qt.Checked:
            pass
        else:
            pass

    def filterChanged(self):
        pass

    def expand(self):
        pass

    def collapse(self):
        pass

    def slotCopyPath(self):
      QApplication.clipboard().setText(self.lblNodePath.text())


    def setContent(self, metaProvider):
        self.metaProvider = metaProvider

        # load main model
        #self.file = QFile(metaFilePath)
        self.metaXML = QDomDocument()
        metadata = self.metaProvider.getMetadata().encode("utf-8")
        self.metaXML.setContent(metadata)

        root = self.metaXML.documentElement()
        n = root.firstChild()
        while not n.isNull():
            item = _getItemForNode(n)
            n = n.nextSibling()
            if item is not None:
                self.treeFull.addTopLevelItem(item)

        self.btnSave.setEnabled(False)

    def itemSelected(self, item, column):
        self.applyEdits()
        self.textValue.clear()
        if isinstance(item, ValueItem):
            self.text = item.value
            self.textValue.setPlainText(self.text)
            self.lastValueItem = item
            self.groupBox.setEnabled(True)
        else:
            self.lastValueItem = None
            self.groupBox.setEnabled(False)

        path = getPath(item)
        self.lblNodePath.setText(path)

    def tabChanged(self, tab):
      if tab == 1:
          standard = MetaInfoStandard.tryDetermineStandard(self.metaProvider)
          if standard == MetaInfoStandard.ISO19115:
              xsltFilePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "metadata", "xsl", "iso19115.xsl")
          if standard == MetaInfoStandard.FGDC:
              xsltFilePath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "metadata", "xsl", "fgdc.xsl")
          xsltFile = QFile(xsltFilePath)
          xsltFile.open(QIODevice.ReadOnly)
          xslt = unicode(xsltFile.readAll())
          xsltFile.close()

          src = self.metaProvider.getMetadata()

          # translate
          qry = QXmlQuery(QXmlQuery.XSLT20)

          '''self.handler = ErrorHandler(self.tr("Translation error"))
          qry.setMessageHandler(self.handler)'''

          qry.setFocus(src)
          qry.setQuery(xslt)

          result = qry.evaluateToString()

          if result:
            #QXmlPattern not support CDATA section
            result = result.replace('&amp;', '&')
            result = result.replace('&gt;', '>')
            result = result.replace('&lt;', '<')

            self.webView.setHtml(result)


    def valueModified(self):
        self.btnSave.setEnabled(True)

    def applyEdits(self):
        if self.lastValueItem is not None:
            value = self.textValue.toPlainText()
            self.lastValueItem.value = value
            node = self.lastValueItem.node
            if not node.hasChildNodes():
                textNode = node.ownerDocument().createTextNode(value)
                node.appendChild(textNode)
            else:
                node.childNodes().at(0).setNodeValue(value)


    def saveMetadata(self):
      try:
        self.metaProvider.setMetadata(unicode(self.metaXML.toString()))
        # TODO: create preview image if need
        self.btnSave.setEnabled(False)
      except:
        QMessageBox.warning(self,
                            self.tr("Error saving metadata"),
                            self.tr("Metadata can't be saved:\n") + unicode(sys.exc_info()[0])
                           )


    def accept(self):
      #TODO check that there is no need to save
      QDialog.accept(self)

def getPath(node):
  path = ""
  if not node.parentNode().isNull() and node.parentNode().nodeType() != QDomNode.DocumentNode:
    path = getPath(node.parentNode()) + " -> "

  return path + node.nodeName()

def _getItemForNode(node):
    subnodes = node.childNodes()

    if subnodes.isEmpty():
        return None
    elif subnodes.at(0).nodeType() == QDomNode.TextNode:
        return subnodes.at(0).toText().nodeValue()
    else:
        item = NodeItem(node)
        for i in xrange(subnodes.length()):
            n = subnodes.at(i)
            ret = _getItemForNode(n)
            if isinstance(ret, (NodeItem, ValueItem)):
                item.addChild(ret)
            else:
                return ValueItem(n, node.nodeName(), ret)
        return item

class NodeItem(QTreeWidgetItem):
    def __init__(self, node):
        QTreeWidgetItem.__init__(self)
        self.node = node
        self.setText(0, node.nodeName())
        #self.setIcon(0, None)

class ValueItem(QTreeWidgetItem):
    def __init__(self, node, name, value):
        QTreeWidgetItem.__init__(self)
        self.node = node
        self.name = name
        self.value = value
        self.setText(0, self.name)


