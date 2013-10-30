from PyQt4 import QtGui, QtCore
from opengeo.qgis import layers

class StyleFromLayerDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(StyleFromLayerDialog, self).__init__(parent)        
        self.layer = None        
        self.name = None
        self.initGui()
        
        
    def initGui(self):                         
        verticalLayout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        self.setWindowTitle('Create style from layer')
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        layerLabel = QtGui.QLabel('Layer')
        layerLabel.setMinimumWidth(150)
        self.layerBox = QtGui.QComboBox()
        self.alllayers = [layer.name() for layer in layers.getAllLayers()]
        self.layerBox.addItems(self.alllayers)
        self.layerBox.setMinimumWidth(250)
        horizontalLayout.addWidget(layerLabel)
        horizontalLayout.addWidget(self.layerBox)
        verticalLayout.addLayout(horizontalLayout)
               
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Name')
        nameLabel.setMinimumWidth(150)
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('')
        self.nameBox.setPlaceholderText("[Use layer name]")
        self.nameBox.setMinimumWidth(250)
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("")
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox) 
        layout.addWidget(buttonBox)
              
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,150)               
    
    def okPressed(self):
        self.layer = self.layerBox.currentText()
        self.name = unicode(self.nameBox.text())
        self.name = self.name if not self.name.strip() == "" else self.layer        
        self.close()

    def cancelPressed(self):
        self.layer = None
        self.name = None
        self.close()  
        
class AddStyleToLayerDialog(QtGui.QDialog):
    
    def __init__(self, catalog, parent = None):
        super(AddStyleToLayerDialog, self).__init__(parent)
        self.catalog = catalog
        self.style = None            
        self.default = None
        self.initGui()        
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        self.setWindowTitle('Add style to layer')
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        styleLabel = QtGui.QLabel('Style')
        self.styleBox = QtGui.QComboBox()
        styles = [style.name for style in self.catalog.get_styles()]
        self.styleBox.addItems(styles)
        horizontalLayout.addWidget(styleLabel)
        horizontalLayout.addWidget(self.styleBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)                
        self.checkBox = QtGui.QCheckBox("Add as default style")        
        horizontalLayout.addWidget(self.checkBox)        
        layout.addLayout(horizontalLayout)
               
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,200)               
    
    def okPressed(self):
        self.style = self.catalog.get_style(self.styleBox.currentText())
        self.default = self.checkBox.isChecked()        
        self.close()

    def cancelPressed(self):
        self.style = None
        self.default = None
        self.close()  
        

class PublishStyleDialog(QtGui.QDialog):
    
    def __init__(self, catalogs, parent = None):
        super(PublishStyleDialog, self).__init__(parent)
        self.catalogs = catalogs            
        self.catalog = None
        self.name = None
        self.initGui()
        
        
    def initGui(self):                         
        verticalLayout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        self.setWindowTitle('Publish style')
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        catalogLabel = QtGui.QLabel('Catalog')
        self.catalogBox = QtGui.QComboBox()        
        self.catalogBox.addItems(self.catalogs)
        horizontalLayout.addWidget(catalogLabel)
        horizontalLayout.addWidget(self.catalogBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Name')
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('')
        self.nameBox.setPlaceholderText("[Use layer name]")
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        verticalLayout.addLayout(horizontalLayout)
               

        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("")
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox) 
        layout.addWidget(buttonBox)
                               
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,200)               
    
    def okPressed(self):        
        self.name = unicode(self.nameBox.text())
        self.name = self.name if not self.name.strip() == "" else None
        self.catalog = self.catalogs[self.catalogBox.currentIndex()]
        self.close()

    def cancelPressed(self):
        self.catalog = None        
        self.name = None
        self.close()          