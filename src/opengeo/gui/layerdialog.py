from PyQt4 import QtGui, QtCore


class PublishLayerDialog(QtGui.QDialog):
    
    def __init__(self, catalogs, parent = None):
        super(PublishLayerDialog, self).__init__(parent)
        self.catalogs = catalogs            
        self.catalog = None
        self.workspace = None
        self.initGui()
        
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        self.setWindowTitle('Publish layer')
         
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        catalogLabel = QtGui.QLabel('Catalog')
        self.catalogBox = QtGui.QComboBox()        
        self.catalogBox.addItems(self.catalogs.keys())
        self.catalogBox.currentIndexChanged.connect(self.catalogHasChanged)
        horizontalLayout.addWidget(catalogLabel)
        horizontalLayout.addWidget(self.catalogBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        workspaceLabel = QtGui.QLabel('Workspace')
        self.workspaceBox = QtGui.QComboBox()     
        self.workspaces = self.catalogs[self.catalogs.keys()[0]].get_workspaces()
        workspaceNames = [w.name for w in self.workspaces]
        self.workspaceBox.addItems(workspaceNames)
        horizontalLayout.addWidget(workspaceLabel)
        horizontalLayout.addWidget(self.workspaceBox)
        layout.addLayout(horizontalLayout)
                      
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200) 
        
    def catalogHasChanged(self):
        catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspaces = catalog.get_workspaces()
        workspaceNames = [w.name for w in self.workspaces]
        self.workspaceBox.clear()
        self.workspaceBox.addItems(workspaceNames)              
    
    def okPressed(self):                
        self.catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspace = self.workspaces[self.workspaceBox.currentIndex()]
        self.close()

    def cancelPressed(self):
        self.catalog = None        
        self.workspace = None
        self.close()          
        
        
        
class PublishLayersDialog(QtGui.QDialog):
    
    def __init__(self, catalogs, layers, parent = None):
        super(PublishLayersDialog, self).__init__(parent)
        self.catalogs = catalogs        
        self.layers = layers
        self.topublish = None        
        self.initGui()
        
        
    def initGui(self):
        self.resize(500, 300)                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        self.setWindowTitle('Publish layers')         
        self.table = QtGui.QTableWidget(None)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0,300)
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(["Catalog", "Workspace"])
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)            
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setTableContent()        

        layout.addWidget(self.table)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
    def setTableContent(self):        
        self.table.setRowCount(len(self.layers))
        layernames = [layer.name() for layer in self.layers]
        self.table.setVerticalHeaderLabels(layernames)
        for idx, layer in enumerate(self.layers):
            catalogBox = QtGui.QComboBox()        
            catalogBox.addItems(self.catalogs.keys())
            catalogBox.currentIndexChanged.connect(self.catalogHasChanged)
            self.table.setCellWidget(idx, 0, catalogBox)                        
            workspaceBox = QtGui.QComboBox()     
            workspaces = self.catalogs[self.catalogs.keys()[0]].get_workspaces()
            workspaceNames = [w.name for w in workspaces]
            workspaceBox.addItems(workspaceNames)
            self.table.setCellWidget(idx, 1, workspaceBox)
    
    def catalogHasChanged(self):
        catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspaces = catalog.get_workspaces()
        workspaceNames = [w.name for w in self.workspaces]
        workspaceBox = self.table.item(self.table.currentRow(), 1)
        workspaceBox.clear()
        workspaceBox.addItems(workspaceNames)              
    
    def okPressed(self):
        self.topublish = []
        for idx, layer in enumerate(self.layers):
            catalogBox = self.table.cellWidget(idx, 0)
            catalog = self.catalogs[catalogBox.currentText()]
            workspaceBox = self.table.cellWidget(idx, 1)
            workspaces = catalog.get_workspaces()
            workspace = workspaces[workspaceBox.currentIndex()]
            self.topublish.append((layer, catalog, workspace))
        self.close()

    def cancelPressed(self):
        self.topublish = None                
        self.close()             
        
        