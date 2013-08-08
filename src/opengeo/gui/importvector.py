from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *

class ImportIntoPostGISDialog(QDialog):
	
	def __init__(self, connection, schema = None, files = None):
		QDialog.__init__(self) 
		self.connection = connection
		self.files = files 		
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
		self.horizontalLayout2 = QHBoxLayout()
		self.schemaLabel = QLabel("Schema")
		self.horizontalLayout2.addWidget(self.schemaLabel)
		self.schemaBox = QComboBox()
		schemas = [schema.name for schema in self.connection.schemas()]
		self.schemaBox.addItems(schemas)
		if self.schema is not None:
			self.schemaBox.setEnabled(False)
		else:
			self.schemaBox.currentIndexChanged.connect(self.updateSchemas)
		self.horizontalLayout2.addWidget(self.schemaBox)
		self.verticalLayout2.addLayout(self.horizontalLayout2)
		self.horizontalLayout3 = QHBoxLayout()   
		self.tableLabel = QLabel("Table")
		self.horizontalLayout3.addWidget(self.tableLabel)
		self.tableBox = QComboBox()
		schemas = self.connection.schemas()
		if schemas:
			tables = [table.name for table in schemas[0].tables()]
			tables.append("[use file name]")
			self.tableBox.addItems(tables)
		self.tableBox.setEditable(True)		
		self.tableBox.currentIndexChanged.connect(self.tableChanged)
		self.horizontalLayout3.addWidget(self.tableBox)
		self.verticalLayout2.addLayout(self.horizontalLayout3)
		self.destinationGroupBox.setLayout(self.verticalLayout2)
		self.verticalLayout.addWidget(self.destinationGroupBox)
		
		self.optionsGroupBox = QGroupBox()
		self.optionsGroupBox.setTitle("Options")
		self.horizontalLayout4 = QHBoxLayout()
		self.addCheckBox = QCheckBox("Add to table (do not overwrite)")
		self.horizontalLayout4.addWidget(self.addCheckBox)
		self.optionsGroupBox.setLayout(self.horizontalLayout4)
		self.verticalLayout.addWidget(self.optionsGroupBox)   

		self.spacer = QSpacerItem(20,40, QSizePolicy.Minimum,QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.spacer)

		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.verticalLayout.addWidget(self.buttonBox)
		
		self.layerBox.setFiles(self.files)
		
		self.setLayout(self.verticalLayout)

		self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
		self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
	
	def tableChanged(self):
		table = self.tableBox.currentText()
		if table != "[use file name]" and self.files is not None and len(self.files) > 1:
			self.addCheckBox.setChecked(True)
			self.addCheckBox.setEnabled(False)
		else:
			self.addCheckBox.setEnabled(True)
			
	def updateSchemas(self):
		name = self.schemaBox.currentText()
		schemas = self.connection.schemas()
		for schema in schemas:
			if schema.name == name:
				self.tableBox.clear()				
				tables = [table.name for table in schema.tables()]
				tables.append("[use file name]")
				self.tableBox.addItems(tables)

	def accept(self):		
		if self.files is None:
			self.layerBox.text.setStyleSheet("QLineEdit{background: yellow}")
			return
		self.ok = True
		self.schema = self.schemaBox.currentText()
		self.tablename = self.tableBox.currentText()
		if self.tablename == "[use file name]":
			self.tablename = None	
		self.add = self.addCheckBox.isChecked()		
		QDialog.accept(self)        
		
	def reject(self):
		self.ok = False
		self.files = None
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
		self.parent.files = files		

	def showSelectionDialog(self):
		vectorFormats = QgsProviderRegistry.instance().fileVectorFilters()
		ret = QFileDialog.getOpenFileNames(self, "Import files", "", vectorFormats)
		if ret:
			files = list(ret)
			self.setFiles(files)

		
		
	   