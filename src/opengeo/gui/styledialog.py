from PyQt4 import QtGui, QtCore
from opengeo.qgis import layers

class StyleFromLayerDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(StyleFromLayerDialog, self).__init__(parent)
        self.layer = None        
        self.name = None
        self.initGui()
        
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        layerLabel = QtGui.QLabel('Layer')
        self.layerBox = QtGui.QComboBox()
        self.alllayers = [layer.name() for layer in layers.get_all_layers()]
        self.layerBox.addItems(self.alllayers)
        horizontalLayout.addWidget(layerLabel)
        horizontalLayout.addWidget(self.layerBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Name')
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('')
        self.nameBox.setPlaceholderText("[Use layer name]")
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)
               
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)               
    
    def okPressed(self):
        self.layer = self.layerBox.currentText()
        self.name = unicode(self.nameBox.text())
        self.name = self.name if not self.name.strip() == "" else self.layer.name() 
        self.close()

    def cancelPressed(self):
        self.layer = None
        self.name = None
        self.close()  
        
class AddStyleToLayerDialog(QtGui.QDialog):
    
    def __init__(self, catalog, parent = None):
        super(AddStyleToLayerDialog, self).__init__(parent)
        self.catalog = catalog
        self.layer = None            
        self.name = None
        self.initGui()        
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
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

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)               
    
    def okPressed(self):
        self.style = self.catalog.get_style(self.styleBox.currentText())
        self.default = self.checkBox.isChecked()        
        self.close()

    def cancelPressed(self):
        self.style = None
        self.default = None
        self.close()  