# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : DB Manager
Description          : Database manager plugin for QGIS
Date                 : Oct 13, 2011
copyright            : (C) 2011 by Giuseppe Sucameli
email                : brush.tyler@gmail.com

The content of this file is based on
- PG_Manager by Martin Dobias (GPLv2 license)
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_DlgCreateTable import Ui_DbManagerDlgCreateTable as Ui_Dialog



class DlgCreateTable(QDialog, Ui_Dialog):
	GEOM_TYPES = ["POINT", "LINESTRING", "POLYGON", "MULTIPOINT", "MULTILINESTRING", "MULTIPOLYGON", "GEOMETRYCOLLECTION"]

	def __init__(self, connection, parent=None):
		QDialog.__init__(self, parent)
		
		self.setupUi(self)
		
		self.fields.setSelectionBehavior(QAbstractItemView.SelectRows);
		
		self.fieldTypes = self.GEOM_TYPES
		self.fields.setColumnCount(3)
		self.fields.setColumnWidth(0,140)
		self.fields.setColumnWidth(1,140)
		self.fields.setColumnWidth(2,50)

		b = QPushButton("Create")
		self.buttonBox.addButton(b, QDialogButtonBox.ActionRole)

		self.connect(self.btnAddField, SIGNAL("clicked()"), self.addField)
		self.connect(self.btnDeleteField, SIGNAL("clicked()"), self.deleteField)
		self.connect(self.btnFieldUp, SIGNAL("clicked()"), self.fieldUp)
		self.connect(self.btnFieldDown, SIGNAL("clicked()"), self.fieldDown)
		self.connect(self.chkGeomColumn, SIGNAL("clicked()"), self.updateUi)
		self.connect(self.fields.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.updateUiFields)
		#self.connect(self., SIGNAL("columnNameChanged()"), self.updatePkeyCombo)

		self.updateUi()
		self.updateUiFields()


	def updateUi(self):
		useGeom = self.chkGeomColumn.isChecked()
		self.cboGeomType.setEnabled(useGeom)
		self.editGeomColumn.setEnabled(useGeom)
		self.spinGeomDim.setEnabled(useGeom)
		self.editGeomSrid.setEnabled(useGeom)
		self.chkSpatialIndex.setEnabled(useGeom)

	def updateUiFields(self):
		print "moco"
		fld = self.selectedField()
		if fld is not None:
			up_enabled = (fld != 0)
			down_enabled = (fld != self.fields.model().rowCount()-1)
			del_enabled = True
		else:
			up_enabled, down_enabled, del_enabled = False, False, False
		self.btnFieldUp.setEnabled(up_enabled)
		self.btnFieldDown.setEnabled(down_enabled)
		self.btnDeleteField.setEnabled(del_enabled)

	def updatePkeyCombo(self, selRow=None):
		""" called when list of columns changes. if 'sel' is None, it keeps current index """

		if selRow is None:
			selRow = self.cboPrimaryKey.currentIndex()

		self.cboPrimaryKey.clear()

		for row in xrange(self.fields.rowCount()):
			widget = self.fields.cellWidget(row, 0)
			name = widget.text()
			self.cboPrimaryKey.addItem(name)

		self.cboPrimaryKey.setCurrentIndex(selRow)

	def addField(self):
		self.fields.setRowCount(self.fields.rowCount()+1)
		self.fields.setRowHeight(self.fields.rowCount()-1, 22)     
		widget = QLineEdit("new_field")   
		self.fields.setCellWidget(self.fields.rowCount()-1, 0, widget)
		typeCombo = QComboBox()
		typeCombo.addItems([
			"integer", "bigint", "smallint", # integers
			"serial", "bigserial", # auto-incrementing ints
			"real", "double precision", "numeric", # floats
			"varchar", "varchar(255)", "char(20)", "text", # strings
			"date", "time", "timestamp"] # date/time
		)
		self.fields.setCellWidget(self.fields.rowCount()-1, 1, typeCombo)        
		nullCombo = QComboBox()
		nullCombo.addItem("Yes")
		nullCombo.addItem("No")
		nullCombo.setCurrentIndex(0)
		self.fields.setCellWidget(self.fields.rowCount()-1, 2, nullCombo)	
		if self.fields.rowCount() == 1:
			typeCombo.setCurrentIndex(3) #serial
		
		self.updatePkeyCombo(0 if self.fields.rowCount() == 1 else None)

	def selectedField(self):
		sel = self.fields.selectedIndexes()
		if len(sel) < 1:
			return None
		return sel[0].row()

	def deleteField(self):
		""" delete selected field """
		row = self.selectedField()
		if row is None:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("no field selected"))
		else:
			self.fields.model().removeRows(row,1)

		self.updatePkeyCombo()

	def fieldUp(self):
		""" move selected field up """
		row = self.selectedField()
		if row is None:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("no field selected"))
			return
		if row == 0:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("field is at top already"))
			return

		# take row and reinsert it
		rowdata = self.fields.model().takeRow(row)
		self.fields.model().insertRow(row-1, rowdata)

		# set selection again
		index = self.fields.model().index(row-1, 0, QModelIndex())
		self.fields.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)

		self.updatePkeyCombo()

	def fieldDown(self):
		""" move selected field down """
		row = self.selectedField()
		if row is None:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("No field selected"))
			return
		if row == self.fields.model().rowCount()-1:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("field is at bottom already"))
			return

		# take row and reinsert it
		rowdata = self.fields.model().takeRow(row)
		self.fields.model().insertRow(row+1, rowdata)

		# set selection again
		index = self.fields.model().index(row+1, 0, QModelIndex())
		self.fields.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)

		self.updatePkeyCombo()

	def createTable(self):
		pass
#===============================================================================
#		""" create table with chosen fields, optionally add a geometry column """
#		if not self.hasSchemas:
#			schema = None
#		else:
#			schema = unicode(self.cboSchema.currentText())
#			if len(schema) == 0:
#				QMessageBox.information(self, self.tr("Sorry"), self.tr("select schema!"))
#				return
# 
#		table = unicode(self.editName.text())
#		if len(table) == 0:
#			QMessageBox.information(self, self.tr("Sorry"), self.tr("enter table name!"))
#			return
# 
#		m = self.fields.model()
#		if m.rowCount() == 0:
#			QMessageBox.information(self, self.tr("Sorry"), self.tr("add some fields!"))
#			return
# 
#		useGeomColumn = self.chkGeomColumn.isChecked()
#		if useGeomColumn:
#			geomColumn = unicode(self.editGeomColumn.text())
#			if len(geomColumn) == 0:
#				QMessageBox.information(self, self.tr("Sorry"), self.tr("set geometry column name"))
#				return
# 
#			geomType = self.GEOM_TYPES[ self.cboGeomType.currentIndex() ]
#			geomDim = self.spinGeomDim.value()
#			try:
#				geomSrid = int(self.editGeomSrid.text())
#			except ValueError:
#				geomSrid = -1
#			useSpatialIndex = self.chkSpatialIndex.isChecked()
# 
#		flds = m.getFields()
#		pk_index = self.cboPrimaryKey.currentIndex()
#		if pk_index >= 0:
#			flds[ pk_index ].primaryKey = True
# 
#		# commit to DB
#		QApplication.setOverrideCursor(Qt.WaitCursor)
#		try:
#			if not useGeomColumn:
#				self.db.createTable(table, flds, schema)
#			else:
#				geom = geomColumn, geomType, geomSrid, geomDim, useSpatialIndex
#				self.db.createVectorTable(table, flds, geom, schema)
# 
#		except (ConnectionError, DbError), e:
#			DlgDbError.showError(e, self)
#			return
# 
#		finally:
#			QApplication.restoreOverrideCursor()
# 
#		QMessageBox.information(self, self.tr("Good"), self.tr("everything went fine"))
#===============================================================================

