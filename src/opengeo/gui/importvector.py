from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ImportIntoPostGISDialog(QDialog):
	
	def __init__(self, connection, schema = None, file = None):
		QDialog.__init__(self) 
		self.connection = connection
		self.file = file 
		self.files = None
		self.schema = schema
		self.tablename = None      
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
		self.layerBox = MultipleFilePanel()
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
		self.horizontalLayout3.addWidget(self.tableBox)
		self.verticalLayout2.addLayout(self.horizontalLayout3)
		self.destinationGroupBox.setLayout(self.verticalLayout2)
		self.verticalLayout.addWidget(self.destinationGroupBox)

		self.spacer = QSpacerItem(20,40, QSizePolicy.Minimum,QSizePolicy.Expanding)
		self.verticalLayout.addItem(self.spacer)

		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.verticalLayout.addWidget(self.buttonBox)
		
		self.setLayout(self.verticalLayout)

		self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
		self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
	
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
			return
		self.schema = self.schemaBox.currentText()
		self.tablename = self.tableBox.currentText()
		if self.tablename == "[use file name]":
			self.tablename = None			
		QDialog.accept(self)        
		
	def reject(self):
		self.files = None
		self.schema = None
		self.tablename = None    
		QDialog.reject(self)
		

class MultipleFilePanel(QWidget):

	def __init__(self, parent = None):
		super(MultipleFilePanel, self).__init__(parent)        
		self.horizontalLayout = QHBoxLayout(self)
		self.horizontalLayout.setSpacing(2)
		self.horizontalLayout.setMargin(0)
		self.label = QLineEdit()
		self.label.setEnabled(False)
		self.label.setText("No files selected")
		#self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self.horizontalLayout.addWidget(self.label)
		self.pushButton = QPushButton()
		self.pushButton.setText("...")
		self.pushButton.clicked.connect(self.showSelectionDialog)
		self.horizontalLayout.addWidget(self.pushButton)
		self.setLayout(self.horizontalLayout)

	def setFiles(self, files):
		self.files = files
		if len(files) > 1:
			self.label.setText(str(len(files)) + " files selected")
		elif len(files) == 0:
			self.label.setText("No files selected")
		else:
			self.label.setText(files[0])

	def showSelectionDialog(self):
		ret = QFileDialog.getOpenFileNames(self, "Import files", "", "All files(*.*)")
		if ret:
			files = list(ret)
			self.setFiles(files)
	   