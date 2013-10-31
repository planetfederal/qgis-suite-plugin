from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *

class ImportIntoPostGISDialog(QDialog):
	
	def __init__(self, connections, connection = None, schema = None, toImport = None):
		QDialog.__init__(self) 
		self.connections = connections
		self.connection = connection
		self.toImport = toImport 		
		self.schema = schema
		self.tablename = None
		self.ok = False 		   
		self.setupUi()

	def setupUi(self):
		self.resize(300, 300)
		self.setWindowTitle('Import into PostGIS')
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
		self.setSizePolicy(sizePolicy)
		
		self.verticalLayout = QVBoxLayout()
		
		self.layersGroupBox = QGroupBox()
		self.layersGroupBox.setTitle("Layers")
		self.horizontalLayout = QHBoxLayout()
		self.layerBox = MultipleFilePanel(self)		
		self.horizontalLayout.addWidget(self.layerBox)
		self.layersGroupBox.setLayout(self.horizontalLayout)
		self.verticalLayout.addWidget(self.layersGroupBox)        

		self.destinationGroupBox = QGroupBox()
		self.destinationGroupBox.setTitle("Destination table")
		self.verticalLayout2 = QVBoxLayout()		
		self.horizontalLayout1 = QHBoxLayout()
		self.connectionLabel = QLabel("Database")
		self.horizontalLayout1.addWidget(self.connectionLabel)
		self.connectionBox = QComboBox()
		connections = [c.name for c in self.connections]
		self.connectionBox.addItems(connections)
		if self.connection is not None:
			self.connectionBox.setCurrentIndex(connections.index(self.connection.name))
			self.connectionBox.setEnabled(False)
		else:
			self.connection = self.connections[0]
			self.connectionBox.currentIndexChanged.connect(self.updateSchemas)
		self.horizontalLayout1.addWidget(self.connectionBox)
		self.verticalLayout2.addLayout(self.horizontalLayout1)
		self.horizontalLayout2 = QHBoxLayout()
		self.schemaLabel = QLabel("Schema")
		self.horizontalLayout2.addWidget(self.schemaLabel)
		self.schemaBox = QComboBox()
		schemas = [schema.name for schema in self.connection.schemas()]
		self.schemaBox.addItems(schemas)
		if self.schema is not None:
			self.schemaBox.setCurrentIndex(schemas.index(self.schema.name))
			self.schemaBox.setEnabled(False)
		else:
			self.schemaBox.currentIndexChanged.connect(self.updateTables)
		self.horizontalLayout2.addWidget(self.schemaBox)
		self.verticalLayout2.addLayout(self.horizontalLayout2)		
		self.horizontalLayout3 = QHBoxLayout()   
		self.tableLabel = QLabel("Table")
		self.horizontalLayout3.addWidget(self.tableLabel)
		self.tableBox = QComboBox()
		schemas = self.connection.schemas()
		tables = [table.name for table in schemas[0].tables()]
		tables.append("[use file name]")
		self.tableBox.addItems(tables)		
		self.tableBox.setEditable(True)
		self.tableBox.setEditText("[use file name]")		
		self.tableBox.currentIndexChanged.connect(self.tableChanged)
		self.tableBox.editTextChanged.connect(self.tableChanged)
		self.horizontalLayout3.addWidget(self.tableBox)
		self.verticalLayout2.addLayout(self.horizontalLayout3)
		self.destinationGroupBox.setLayout(self.verticalLayout2)
		self.verticalLayout.addWidget(self.destinationGroupBox)
		
		self.optionsGroupBox = QGroupBox()
		self.optionsGroupBox.setTitle("Options")
		self.horizontalLayout4 = QHBoxLayout()
		self.addCheckBox = QCheckBox("Add to table (do not overwrite)")
		self.horizontalLayout4.addWidget(self.addCheckBox)
		self.singleGeomCheckBox = QCheckBox("Import as single geometries")
		self.horizontalLayout4.addWidget(self.singleGeomCheckBox)
		self.optionsGroupBox.setLayout(self.horizontalLayout4)
		self.verticalLayout.addWidget(self.optionsGroupBox)   

		self.spacer = QSpacerItem(20,40, QSizePolicy.Minimum,QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.spacer)

		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.verticalLayout.addWidget(self.buttonBox)
		
		self.layerBox.setFiles(self.toImport)		
		
		self.setLayout(self.verticalLayout)

		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
	
	def tableChanged(self):
		table = self.tableBox.currentText()
		if table != "[use file name]" and self.toImport is not None and len(self.toImport) > 1:
			self.addCheckBox.setChecked(True)
			self.addCheckBox.setEnabled(False)
		else:
			self.addCheckBox.setEnabled(True)
			
	def updateSchemas(self):
		name = self.connectionBox.currentText()		
		for c in self.connections:
			if c.name == name:
				self.connection = c
				self.schemaBox.clear()				
				schemas = [schema.name for schema in c.schemas()]				
				self.tableBox.addItems(schemas)
				self.updateTables()
				break
							
	def updateTables(self):
		name = self.schemaBox.currentText()
		schemas = self.connection.schemas()
		for schema in schemas:
			if schema.name == name:
				self.tableBox.clear()				
				tables = [table.name for table in schema.tables()]
				tables.append("[use file name]")
				self.tableBox.addItems(tables)

	def accept(self):		
		if self.toImport is None:
			self.layerBox.text.setStyleSheet("QLineEdit{background: yellow}")
			return		
		schema = self.schemaBox.currentText()
		if schema == "":
			self.schemaBox.text.setStyleSheet("QLineEdit{background: yellow}")
			return
		self.schema = schema
		self.tablename = self.tableBox.currentText()
		if self.tablename == "[use file name]" or self.tablename == "":
			self.tablename = None	
		self.add = self.addCheckBox.isChecked()
		self.single = self.singleGeomCheckBox.isChecked()
		self.ok = True		
		QDialog.accept(self)        
		
	def reject(self):		
		self.ok = False
		self.toImport = None
		self.schema = None
		self.tablename = None    
		QDialog.reject(self)
		

class MultipleFilePanel(QWidget):

	def __init__(self, parent):
		super(MultipleFilePanel, self).__init__(parent) 
		self.parent = parent       
		self.horizontalLayout = QHBoxLayout(self)
		self.horizontalLayout.setSpacing(2)
		self.horizontalLayout.setMargin(0)
		self.text = QLineEdit()
		self.text.setEnabled(False)
		self.text.setText("No files selected")		
		self.horizontalLayout.addWidget(self.text)
		self.pushButton = QPushButton()
		self.pushButton.setText("...")
		self.pushButton.clicked.connect(self.showSelectionDialog)
		self.horizontalLayout.addWidget(self.pushButton)
		self.setLayout(self.horizontalLayout)
		self.files = None

	def setFiles(self, files):
		if files is None:
			return
		if files and isinstance(files[0], QgsMapLayer):
			self.text.setText(str(len(files)) + " layers selected")
			self.pushButton.setEnabled(False)	
			return
		if len(files) > 1:
			table = self.parent.tableBox.currentText()
			if table != "[use file name]":
				self.parent.addCheckBox.setChecked(True)
				self.parent.addCheckBox.setEnabled(False)
			self.text.setText(str(len(files)) + " files selected")			
		elif len(files) == 0:
			self.text.setText("No files selected")			
			self.parent.addCheckBox.setEnabled(True)
		else:
			self.text.setText(files[0])
			self.parent.addCheckBox.setEnabled(True)
		self.parent.toImport = files		

	def showSelectionDialog(self):
		vectorFormats = QgsProviderRegistry.instance().fileVectorFilters()
		ret = QFileDialog.getOpenFileNames(self, "Import files", "", vectorFormats)
		if ret:
			files = list(ret)
			self.setFiles(files)

		
		
	   