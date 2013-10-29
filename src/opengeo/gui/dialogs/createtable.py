# -*- coding: utf-8 -*-
'''based on the code by Giuseppe Sucameli and Martin Dobias'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo.postgis.postgis_utils import TableField


class DlgCreateTable(QDialog):
	GEOM_TYPES = ["POINT", "LINESTRING", "POLYGON", "MULTIPOINT", "MULTILINESTRING", "MULTIPOLYGON", "GEOMETRYCOLLECTION"]

	def __init__(self, connection, parent=None):
		QDialog.__init__(self, parent)		
		self.ok = False		
		self.setupUi()
		
		self.table.setSelectionBehavior(QAbstractItemView.SelectRows);
		
		self.fieldTypes = self.GEOM_TYPES
		self.table.setColumnCount(3)
		self.table.setColumnWidth(0,140)
		self.table.setColumnWidth(1,140)
		self.table.setColumnWidth(2,50)

		self.connect(self.btnAddField, SIGNAL("clicked()"), self.addField)
		self.connect(self.btnDeleteField, SIGNAL("clicked()"), self.deleteField)
		self.connect(self.chkGeomColumn, SIGNAL("clicked()"), self.updateUi)
		self.connect(self.table.selectionModel(), SIGNAL("selectionChanged(const QItemSelection &, const QItemSelection &)"), self.updateUiFields)
		self.connect(self.buttonBox, SIGNAL("accepted()"), self.okPressed)
		self.connect(self.buttonBox, SIGNAL("rejected()"), self.cancelPressed)

		self.updateUi()
		self.updateUiFields()

	def setupUi(self):		
		self.resize(500, 600)
		self.gridLayout_2 = QGridLayout(self)		
		self.gridlayout = QGridLayout()			 
		self.label = QLabel(self)
		self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)		
		self.gridlayout.addWidget(self.label, 1, 0, 1, 2)
		self.editName = QLineEdit(self)				
		self.gridlayout.addWidget(self.editName, 1, 2, 1, 1)
		self.gridLayout_2.addLayout(self.gridlayout, 0, 0, 1, 2)
		self.vboxlayout = QVBoxLayout()		
		self.btnAddField = QPushButton(self)		
		self.vboxlayout.addWidget(self.btnAddField)
		self.btnDeleteField = QPushButton(self)		
		self.vboxlayout.addWidget(self.btnDeleteField)
		spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.vboxlayout.addItem(spacerItem)
		#=======================================================================
		# self.btnFieldUp = QPushButton(self)		
		# self.vboxlayout.addWidget(self.btnFieldUp)
		# self.btnFieldDown = QPushButton(self)		
		# self.vboxlayout.addWidget(self.btnFieldDown)
		#=======================================================================
		self.gridLayout_2.addLayout(self.vboxlayout, 1, 1, 1, 1)
		self.hboxlayout = QHBoxLayout()
		self.hboxlayout.setSpacing(8)		
		self.label_4 = QLabel(self)		
		self.hboxlayout.addWidget(self.label_4)
		self.cboPrimaryKey = QComboBox(self)
		sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.cboPrimaryKey.sizePolicy().hasHeightForWidth())
		self.cboPrimaryKey.setSizePolicy(sizePolicy)		
		self.hboxlayout.addWidget(self.cboPrimaryKey)
		self.gridLayout_2.addLayout(self.hboxlayout, 2, 0, 1, 2)
		self.gridLayout = QGridLayout()		
		self.chkGeomColumn = QCheckBox(self)	   
		self.gridLayout.addWidget(self.chkGeomColumn, 0, 0, 1, 1)
		self.cboGeomType = QComboBox(self)
		self.cboGeomType.addItems(self.GEOM_TYPES)		
		self.gridLayout.addWidget(self.cboGeomType, 0, 1, 1, 2)
		self.label_2 = QLabel(self)
		self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)		
		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
		self.editGeomColumn = QLineEdit(self)
		self.editGeomColumn.setText("geom")		
		self.gridLayout.addWidget(self.editGeomColumn, 1, 1, 1, 1)
		self.label_5 = QLabel(self)
		self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)		
		self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
		self.spinGeomDim = QSpinBox(self)
		self.spinGeomDim.setMinimum(2)
		self.spinGeomDim.setMaximum(4)		
		self.gridLayout.addWidget(self.spinGeomDim, 2, 1, 1, 1)
		spacerItem1 = QSpacerItem(50, 51, QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 2, 2, 2, 1)
		self.label_6 = QLabel(self)
		self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)		
		self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
		self.editGeomSrid = QLineEdit(self)
		self.editGeomSrid.setText("-1")		
		self.gridLayout.addWidget(self.editGeomSrid, 3, 1, 1, 1)
		self.chkSpatialIndex = QCheckBox(self)		
		self.gridLayout.addWidget(self.chkSpatialIndex, 4, 0, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 2)
		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Close | QDialogButtonBox.Ok)		
		self.gridLayout_2.addWidget(self.buttonBox, 4, 0, 1, 2)
		self.table = QTableWidget(self)		
		self.table.setColumnCount(3)  		
		self.table.setHorizontalHeaderLabels(["Name", "Type", "Null"])
		self.table.horizontalHeader().setStretchLastSection(True) 
		self.table.resizeRowsToContents()  
		self.gridLayout_2.addWidget(self.table, 1, 0, 1, 1)				
		QMetaObject.connectSlotsByName(self)		
		self.setTabOrder(self.editName, self.table)
		self.setTabOrder(self.table, self.btnAddField)
		self.setTabOrder(self.btnAddField, self.btnDeleteField)
		#self.setTabOrder(self.btnDeleteField, self.btnFieldUp)
		#self.setTabOrder(self.btnFieldUp, self.btnFieldDown)
		self.setTabOrder(self.btnDeleteField, self.cboPrimaryKey)
		self.setTabOrder(self.cboPrimaryKey, self.chkGeomColumn)
		self.setTabOrder(self.chkGeomColumn, self.cboGeomType)
		self.setTabOrder(self.cboGeomType, self.editGeomColumn)
		self.setTabOrder(self.editGeomColumn, self.spinGeomDim)
		self.setTabOrder(self.spinGeomDim, self.editGeomSrid)
		self.setTabOrder(self.editGeomSrid, self.chkSpatialIndex)
		self.setTabOrder(self.chkSpatialIndex, self.buttonBox)
		self.setWindowTitle("Create Table")
		self.chkSpatialIndex.setText("Create spatial index")
		self.label.setText("Name")
		self.btnAddField.setText("Add field")
		self.btnDeleteField.setText("Delete field")
		#self.btnFieldUp.setText("Up")
		#self.btnFieldDown.setText("Down")
		self.label_4.setText("Primary key")
		self.chkGeomColumn.setText("Create geometry column")
		self.label_2.setText("Name")
		self.label_5.setText("Dimensions")
		self.label_6.setText("SRID")

	def updateUi(self):
		useGeom = self.chkGeomColumn.isChecked()
		self.cboGeomType.setEnabled(useGeom)
		self.editGeomColumn.setEnabled(useGeom)
		self.spinGeomDim.setEnabled(useGeom)
		self.editGeomSrid.setEnabled(useGeom)
		self.chkSpatialIndex.setEnabled(useGeom)

	def updateUiFields(self):	   
		fld = self.selectedField()
		if fld is not None:
			up_enabled = (fld != 0)
			down_enabled = (fld != self.table.model().rowCount()-1)
			del_enabled = True
		else:
			up_enabled, down_enabled, del_enabled = False, False, False
		#self.btnFieldUp.setEnabled(up_enabled)
		#self.btnFieldDown.setEnabled(down_enabled)
		self.btnDeleteField.setEnabled(del_enabled)

	def updatePkeyCombo(self, selRow=None):
		""" called when list of columns changes. if 'sel' is None, it keeps current index """

		if selRow is None:
			selRow = self.cboPrimaryKey.currentIndex()

		self.cboPrimaryKey.clear()

		for row in xrange(self.table.rowCount()):
			widget = self.table.cellWidget(row, 0)
			name = widget.text()
			self.cboPrimaryKey.addItem(name)

		self.cboPrimaryKey.setCurrentIndex(selRow)

	def addField(self):
		self.table.setRowCount(self.table.rowCount()+1)
		self.table.setRowHeight(self.table.rowCount()-1, 22)	 
		widget = QLineEdit("new_field")   
		widget.textEdited.connect(lambda: self.updatePkeyCombo(None))
		self.table.setCellWidget(self.table.rowCount()-1, 0, widget)
		typeCombo = QComboBox()
		typeCombo.addItems([
			"integer", "bigint", "smallint", # integers
			"serial", "bigserial", # auto-incrementing ints
			"real", "double precision", "numeric", # floats
			"varchar", "varchar(255)", "char(20)", "text", # strings
			"date", "time", "timestamp"] # date/time
		)
		self.table.setCellWidget(self.table.rowCount()-1, 1, typeCombo)		
		nullCombo = QComboBox()
		nullCombo.addItem("Yes")
		nullCombo.addItem("No")
		nullCombo.setCurrentIndex(0)
		self.table.setCellWidget(self.table.rowCount()-1, 2, nullCombo)   
		if self.table.rowCount() == 1:
			typeCombo.setCurrentIndex(3) #serial
		
		self.updatePkeyCombo(0 if self.table.rowCount() == 1 else None)

	def selectedField(self):
		sel = self.table.selectedIndexes()
		if len(sel) < 1:
			return None
		return sel[0].row()

	def deleteField(self):
		""" delete selected field """
		row = self.selectedField()
		if row is None:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("no field selected"))
		else:
			self.table.model().removeRows(row,1)

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
		rowdata = self.table.model().takeRow(row)
		self.table.model().insertRow(row-1, rowdata)

		# set selection again
		index = self.table.model().index(row-1, 0, QModelIndex())
		self.table.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)

		self.updatePkeyCombo()

	def fieldDown(self):
		""" move selected field down """
		row = self.selectedField()
		if row is None:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("No field selected"))
			return
		if row == self.table.model().rowCount()-1:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("field is at bottom already"))
			return

		# take row and reinsert it
		rowdata = self.table.model().takeRow(row)
		self.table.model().insertRow(row+1, rowdata)

		# set selection again
		index = self.table.model().index(row+1, 0, QModelIndex())
		self.table.selectionModel().select(index, QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)

		self.updatePkeyCombo()

	def okPressed(self):
		self.name = unicode(self.editName.text())
		if len(self.name) == 0:
			self.editName.setStyleSheet("QLineEdit{background: yellow}")
			return			  
		if self.table.rowCount() == 0:
			QMessageBox.information(self, self.tr("Sorry"), self.tr("add some fields!"))
			return

		self.useGeomColumn = self.chkGeomColumn.isChecked()
		if self.useGeomColumn:
			self.geomColumn = unicode(self.editGeomColumn.text())
			if len(self.geomColumn) == 0:
				self.editGeomColumn.setStyleSheet("QLineEdit{background: yellow}")
				return
			
			self.geomType = self.GEOM_TYPES[ self.cboGeomType.currentIndex() ]
			self.geomDim = self.spinGeomDim.value()
			try:
				self.geomSrid = int(self.editGeomSrid.text())
			except ValueError:
				self.geomSrid = -1
			self.useSpatialIndex = self.chkSpatialIndex.isChecked()

		self.fields = []
		for i in xrange(self.table.rowCount()):
			name = self.table.cellWidget(i, 0).text()
			type = self.table.cellWidget(i, 1).currentText() 
			null = self.table.cellWidget(i, 2).currentIndex == 0
			self.fields.append(TableField(name, type, null))
		self.pk = self.cboPrimaryKey.currentText()
		self.ok = True
		self.close()
		
	def cancelPressed(self):
		self.ok = False
		self.close()
 


