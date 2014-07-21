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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns  import *

from qgis.core import *
from qgis.gui import *

from ui.ui_viewer import Ui_MetatoolsViewer
from error_handler import ErrorHandler

class MetatoolsViewer(QDialog, Ui_MetatoolsViewer):
  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)
    self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint)

    #set browser context menu
    self.webView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.webView.customContextMenuRequested.connect(self.openMenu)
    self.contextMenu=QMenu()
    self.actionCopy.activated.connect(self.slotCopy)
    self.actionPrint.activated.connect(self.slotPrint)
    self.actionCopyAll.activated.connect(self.slotCopyAll)

  def openMenu(self, position):
    self.contextMenu.clear()
    if self.webView.selectedText():
      self.contextMenu.addAction(self.actionCopy)
    self.contextMenu.addAction(self.actionCopyAll)
    self.contextMenu.addSeparator()
    self.contextMenu.addAction(self.actionPrint)

    self.contextMenu.exec_(self.webView.mapToGlobal(position))

  def slotPrint(self):
    printer = QPrinter()
    dialog = QPrintDialog(printer)
    if dialog.exec_() == QDialog.Accepted:
      self.webView.print_(printer)

  def slotCopyAll(self):
    mimeData=QMimeData()
    mimeData.setHtml(self.webView.page().mainFrame().toHtml())
    mimeData.setText(self.webView.page().mainFrame().toPlainText())
    clipboard = QApplication.clipboard()
    clipboard.setMimeData(mimeData)

  def slotCopy(self):
    if self.webView.selectedText():
      clipboard = QApplication.clipboard()
      clipboard.setText(self.webView.selectedText())

  def setContent(self, metaProvider, xsltFilePath):
    # load data
    xsltFile = QFile(xsltFilePath)
    xsltFile.open(QIODevice.ReadOnly)
    xslt = unicode(xsltFile.readAll())
    xsltFile.close()

    src = metaProvider.getMetadata()

    # translate
    qry = QXmlQuery(QXmlQuery.XSLT20)

    self.handler = ErrorHandler(self.tr("Translation error"))
    qry.setMessageHandler(self.handler)

    qry.setFocus(src)
    qry.setQuery(xslt)

    result = qry.evaluateToString()

    #workaround, for PyQt < 4.8
    #array = ""
    #buf = QBuffer(array)
    #buf.open(QIODevice.WriteOnly)
    #qry.evaluateTo(buf)
    #result = unicode(array)

    if result:
      #QXmlPattern not support CDATA section
      result = result.replace('&amp;', '&')
      result = result.replace('&gt;', '>')
      result = result.replace('&lt;', '<')

      self.webView.setHtml(result) # QString.fromUtf8(result))
      return True
    else:
      return False

  def setHtml(self, html):
    self.webView.setHtml(html)

