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

from qgis.core import *
from qgis.gui import *

import sys
from dom_model import DomModel, FilterDomModel
from ui.ui_editor import Ui_MetatoolsEditor

class MetatoolsEditor(QDialog, Ui_MetatoolsEditor):
  def __init__(self):
    QDialog.__init__(self)
    self.setupUi(self)
    self.setWindowFlags(Qt.Window | Qt.WindowMaximizeButtonHint)

    self.tabWidget.setCurrentIndex(0)
    self.lblNodePath.setText("")

    self.btnSave = self.buttonBox.button(QDialogButtonBox.Save)
    self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

    self.btnApply = QPushButton(self.tr("Apply"))
    self.btnDiscard = QPushButton(self.tr("Discard"))
    self.editorButtonBox.clear()
    self.editorButtonBox.addButton(self.btnApply, QDialogButtonBox.AcceptRole)
    self.editorButtonBox.addButton(self.btnDiscard, QDialogButtonBox.RejectRole)

    #contextmenu
    self.lblNodePath.setContextMenuPolicy(Qt.ActionsContextMenu)
    self.lblNodePath.addAction(self.actionCopyPath)
    self.connect(self.actionCopyPath, SIGNAL("activated()"), self.slotCopyPath)

    # full metadata view
    self.treeFull.clicked.connect(self.itemSelected)
    self.treeFull.collapsed.connect(self.collapsedExpanded)
    self.treeFull.expanded.connect(self.collapsedExpanded)

    # filtered metadata view
    self.tbwFiltered.currentCellChanged.connect(self.cellSelected)

    self.textValue.textChanged.connect(self.valueModified)
    self.tabWidget.currentChanged.connect(self.tabChanged)

    self.btnApply.clicked.connect(self.applyEdits)
    self.btnDiscard.clicked.connect(self.resetEdits)

    self.buttonBox.accepted.disconnect(self.accept)
    self.btnSave.clicked.connect(self.saveMetadata)

  def slotCopyPath(self):
    QApplication.clipboard().setText(self.lblNodePath.text())

  def setContent(self, metaProvider):
    self.metaProvider = metaProvider

    # load main model
    #self.file = QFile(metaFilePath)
    self.metaXML = QDomDocument()
    metadata = self.metaProvider.getMetadata().encode("utf-8")
    self.metaXML.setContent(metadata)
    self.model = DomModel(self.metaXML, self)

    # set full view
    self.treeFull.setModel(self.model)
    self.treeFull.hideColumn(1) # hide attrs
    self.treeFull.resizeColumnToContents(0) # resize value column

    # load filtered list
    self.filteredIndexes = None # lazy init
    # set filtered view
    #self.fillTableWidget()

    self.btnSave.setEnabled(False)

  def itemSelected(self, mindex):
    # Display item selected in TreeView in edit box.
    self.textValue.clear()

    path = ""
    editable = False
    self.text = None

   # full view
    self.mindex = self.model.index(mindex.row(), 2, mindex.parent())
    path = self.model.nodePath(self.mindex)
    editable = self.model.isEditable(self.mindex)
    self.text = self.model.data(self.mindex, 0)

    self.lblNodePath.setText(path)
    if editable:
      self.textValue.setPlainText(self.text)
      self.groupBox.setEnabled(True)
      self.editorButtonBox.setEnabled(False)
    else:
      self.textValue.clear()
      self.groupBox.setEnabled(False)

  def cellSelected(self, currentRow, currentColumn, previousRow, previousColumn):
    # Display item selected in TableWidget in edit box.
    self.textValue.clear()

    path = ""
    editable = False
    self.text = None

    self.mindex = self.filteredIndexes[currentRow][1]
    path = self.model.nodePath(self.mindex)
    editable = self.model.isEditable(self.mindex)
    self.text = self.model.data(self.mindex, 0)

    self.lblNodePath.setText(path)
    if editable:
      self.textValue.setPlainText(self.text)
      self.groupBox.setEnabled(True)
      self.editorButtonBox.setEnabled(False)
    else:
      self.textValue.clear()
      self.groupBox.setEnabled(False)

  def collapsedExpanded(self, mindex):
    if self.tabWidget.currentIndex() == 0:
      self.treeFull.resizeColumnToContents(0)
    else:
      self.tbwFiltered.resizeColumnToContents(0)

  def valueModified(self):
    self.editorButtonBox.setEnabled(True)

  def tabChanged(self, tab):
    self.textValue.clear()

    path = ""
    editable = False
    self.text = None

    if tab == 0:
      mindex = self.treeFull.currentIndex()
      self.mindex = self.model.index(mindex.row(), 2, mindex.parent())
      path = self.model.nodePath(self.mindex)
      editable = self.model.isEditable(self.mindex)
      self.text = self.model.data(self.mindex, 0)
    else:
      # lazy init
      if not self.filteredIndexes:
        filter_lines = self.loadFilter()
        self.filteredIndexes = self.searchNodes(self.model, filter_lines)
        self.tbwFiltered.horizontalHeader().setVisible(True) # pyuic4 bug
        self.tbwFiltered.setRowCount(len(self.filteredIndexes))
      # refresh table
      self.fillTableWidget()
      # refresh selection
      selectedItems = self.tbwFiltered.selectedItems()
      if len(selectedItems):
          self.mindex = self.filteredIndexes[selectedItems[0].row()][1]
          path = self.model.nodePath(self.mindex)
          editable = self.model.isEditable(self.mindex)
          self.text = self.model.data(self.mindex, 0)

    self.lblNodePath.setText(path)
    if editable:
      self.textValue.setPlainText(self.text)
      self.groupBox.setEnabled(True)
      self.editorButtonBox.setEnabled(False)
    else:
      self.textValue.clear()
      self.groupBox.setEnabled(False)

  def applyEdits(self):
    self.model.setData(self.mindex, self.textValue.toPlainText())
    self.text = self.model.data(self.mindex, 0)
    self.btnSave.setEnabled(True)
    self.editorButtonBox.setEnabled(False)
    if self.tabWidget.currentIndex() != 0:
        self.fillTableWidget()

  def resetEdits(self):
    self.textValue.setPlainText(self.text)
    self.editorButtonBox.setEnabled(False)

  def saveMetadata(self):
    try:
      self.metaProvider.setMetadata(unicode(self.metaXML.toString()))
      # TODO: create preview image if need
      self.btnSave.setEnabled(False)
    except:
      QMessageBox.warning(self,
                          self.tr("Metatools"),
                          self.tr("Metadata can't be saved:\n") + unicode(sys.exc_info()[0])
                         )

  def loadFilter(self):
    settings = QSettings("NextGIS", "metatools")
    fileName = settings.value("general/filterFile", "")

    if fileName == "":
      return []

    # read filter from file
    filter_lines = []
    f = QFile(fileName)
    if not f.open(QIODevice.ReadOnly):
      QMessageBox.warning(self,
                          self.tr('I/O error'),
                          self.tr("Can't open file %s") % (fileName)
                         )
      return []

    stream = QTextStream(f)
    while not stream.atEnd():
      line = stream.readLine()
      filter_lines.append(line)
    f.close()

    return filter_lines

  def searchNodes(self, model, filters):
    allItemsIndexes = model.match(model.index(0, 0, QModelIndex()), Qt.DisplayRole, '*', -1, Qt.MatchWildcard | Qt.MatchRecursive)
    searchedItems = []
    for itemIndex in allItemsIndexes:
      if self.model.nodePath(itemIndex) in filters:
        valueItemIndex = self.model.index(0, 2, itemIndex.parent())
        if not self.model.isEditable(itemIndex) and self.model.hasOneGco(itemIndex) :
            valueItemIndex = self.model.index(0, 2, itemIndex)
        searchedItems.append([itemIndex, valueItemIndex])
    return searchedItems

  def fillTableWidget(self):
      row = 0
      for nameItemIndex, valueItemIndex in self.filteredIndexes:
          name = unicode(self.model.data(nameItemIndex, Qt.DisplayRole))
          value = unicode(self.model.data(valueItemIndex, Qt.DisplayRole))
          self.tbwFiltered.setItem(row, 0, QTableWidgetItem(name))
          self.tbwFiltered.setItem(row, 1, QTableWidgetItem(value))
          row += 1

      self.tbwFiltered.resizeColumnToContents(0)

  def accept(self):
    QDialog.accept(self)
