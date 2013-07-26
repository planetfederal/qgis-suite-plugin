from opengeo.gui.ui_gwclayer import Ui_EditGwcLayerDialog
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from opengeo.gui.extentpanel import ExtentSelectionPanel

class EditGwcLayerDialog(QDialog, Ui_EditGwcLayerDialog):
    
    def __init__(self, layer = None):
        QDialog.__init__(self)
        self.setupUi(self)
        if layer is not None:
            self.spinBoxHeight.setValue(layer.metaHeight)
            self.spinBoxWidth.setValue(layer.metaWidth)
            checkboxes = [self.checkBox4326, self.checkBox900913, self.checkBoxGlobalPixel, self.checkBoxGlobalScale, self.checkBoxGoogle]
            for checkbox in checkboxes:                
                checkbox.setChecked(checkbox.text() in layer.gridsets)             
            checkboxes = [self.checkBoxGif, self.checkBoxJpg, self.checkBoxPng, self.checkBoxPng8]
            for checkbox in checkboxes:                
                checkbox.setChecked('image/' + checkbox.text() in layer.mimetypes)
        else:
            self.spinBoxHeight.setValue(4)
            self.spinBoxWidth.setValue(4)
            self.checkBox4326.setChecked(True)
            self.checkBoxPng.setChecked(True)

    def accept(self):
        self.metaWidth = self.spinBoxWidth.value()
        self.metaHeight = self.spinBoxHeight.value()
        checkboxes = [self.checkBox4326, self.checkBox900913, self.checkBoxGlobalPixel, self.checkBoxGlobalScale, self.checkBoxGoogle]
        self.gridsets = [checkbox.text() for checkbox in checkboxes if checkbox.isChecked()]
        checkboxes = [self.checkBoxGif, self.checkBoxJpg, self.checkBoxPng, self.checkBoxPng8]
        self.formats = ['image/' + checkbox.text() for checkbox in checkboxes if checkbox.isChecked()]
        QDialog.accept(self)        
        
    def reject(self):
        self.formats = None
        self.gridsets = None
        self.metaWidth = None
        self.metaHeight = None
        QDialog.reject(self)
        

class SeedGwcLayerDialog(QDialog):
    
    SEED = 0
    RESEED = 1
    TRUNCATE = 2
    
    def __init__(self, layer, parent = None):
        super(SeedGwcLayerDialog, self).__init__(parent)
        self.layer = layer
        self.minzoom = None
        self.maxzoom = None
        self.gridset = None
        self.format = None
        self.operation = None
        self.extent = None
        self.initGui()
        
        
    def initGui(self):                         
        self.setWindowTitle('Seed cache layer')
        layout = QVBoxLayout()                                
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)        
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        operationLabel = QLabel('Operation')
        self.operationBox = QComboBox()      
        operations = ['Seed', 'Reseed', 'Truncate']  
        self.operationBox.addItems(operations)
        horizontalLayout.addWidget(operationLabel)
        horizontalLayout.addWidget(self.operationBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        grisetLabel = QLabel('Gridset')
        self.gridsetBox = QComboBox()              
        self.gridsetBox.addItems(self.layer.gridsets)
        horizontalLayout.addWidget(grisetLabel)
        horizontalLayout.addWidget(self.gridsetBox)
        layout.addLayout(horizontalLayout)    
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        formatLabel = QLabel('Format')
        self.formatBox = QComboBox()              
        self.formatBox.addItems(self.layer.mimetypes)
        horizontalLayout.addWidget(formatLabel)
        horizontalLayout.addWidget(self.formatBox)
        layout.addLayout(horizontalLayout)  
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        minZoomLabel = QLabel('Min zoom')
        self.minZoomBox = QComboBox()      
        levels = [str(i) for i in range(21)]  
        self.minZoomBox.addItems(levels)
        horizontalLayout.addWidget(minZoomLabel)
        horizontalLayout.addWidget(self.minZoomBox)
        layout.addLayout(horizontalLayout)    
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        maxZoomLabel = QLabel('Max zoom')
        self.maxZoomBox = QComboBox()      
        levels = [str(i) for i in range(21)]  
        self.maxZoomBox.addItems(levels)
        horizontalLayout.addWidget(maxZoomLabel)
        horizontalLayout.addWidget(self.maxZoomBox)
        layout.addLayout(horizontalLayout)    
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        extentLabel = QLabel('Bounding box')
        self.extentPanel = ExtentSelectionPanel(self)              
        horizontalLayout.addWidget(extentLabel)
        horizontalLayout.addWidget(self.extentPanel)
        layout.addLayout(horizontalLayout)                                       
        
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(600,250)
            
    
    def okPressed(self):
        self.minzoom = int(self.minZoomBox.currentText())
        self.maxzoom = int(self.maxZoomBox.currentText())
        self.gridset = self.gridsetBox.currentText()
        self.format = self.formatBox.currentText()
        self.operation = self.operationBox.currentIndex() 
        self.extent = None
        self.close()

    def cancelPressed(self):
        self.minzoom = None
        self.maxzoom = None
        self.gridset = None
        self.format = None
        self.operation = None 
        try:
            self.extent =self.extentPanel.getValue()
        except:
            self.extentPanel.text.setStyleSheet("QLineEdit{background: yellow}") 
        self.close() 