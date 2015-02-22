from PyQt4 import QtGui, QtCore

from opengeo.qgis import layers
from opengeo.gui.gsnameutils import GSNameWidget, xmlNameFixUp, \
    xmlNameRegexMsg, xmlNameRegex


class PublishLayerDialog(QtGui.QDialog):
    
    def __init__(self, catalogs, layer=None, parent = None):
        super(PublishLayerDialog, self).__init__(parent)
        self.catalogs = catalogs
        self.layer = layer
        self.catalog = None
        self.workspace = None
        self.layername = None
        self.initGui()
        
        
    def initGui(self):                                             
        self.setWindowTitle('Publish layer')
        layout = QtGui.QVBoxLayout()                                
         
        gridLayout = QtGui.QGridLayout()
        gridLayout.setSpacing(10)
        gridLayout.setMargin(10)
        catalogLabel = QtGui.QLabel('Catalog')
        catalogLabel.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                              QtGui.QSizePolicy.Fixed))
        gridLayout.addWidget(catalogLabel, 0, 0)
        self.catalogBox = QtGui.QComboBox()
        self.catalogBox.addItems(self.catalogs.keys())
        self.catalogBox.currentIndexChanged.connect(self.catalogHasChanged)
        gridLayout.addWidget(self.catalogBox, 0, 1)

        workspaceLabel = QtGui.QLabel('Workspace')
        workspaceLabel.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                              QtGui.QSizePolicy.Fixed))
        gridLayout.addWidget(workspaceLabel, 1, 0)
        self.workspaceBox = QtGui.QComboBox()
        cat = self.catalogs[self.catalogs.keys()[0]]      
        self.workspaces = cat.get_workspaces()
        try:
            defaultWorkspace = cat.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None  
        workspaceNames = [w.name for w in self.workspaces]        
        self.workspaceBox.addItems(workspaceNames)        
        if defaultName is not None:
            self.workspaceBox.setCurrentIndex(workspaceNames.index(defaultName))
        gridLayout.addWidget(self.workspaceBox, 1, 1)

        nameLabel = QtGui.QLabel('Layer')
        nameLabel.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                              QtGui.QSizePolicy.Fixed))
        gridLayout.addWidget(nameLabel, 2, 0)
        gslayers = [lyr.name for lyr in cat.get_layers()]
        self.nameBox = GSNameWidget(
            name=xmlNameFixUp(self.layer.name()),
            nameregex=xmlNameRegex(),
            nameregexmsg=xmlNameRegexMsg(),
            names=gslayers,
            unique=False)
        gridLayout.addWidget(self.nameBox, 2, 1)
        
        self.destGroupBox = QtGui.QGroupBox()
        self.destGroupBox.setLayout(gridLayout)
        
        layout.addWidget(self.destGroupBox)
        
        self.spacer = QtGui.QSpacerItem(20,40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(self.spacer)
                      
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.nameBox.nameValidityChanged.connect(self.okButton.setEnabled)
        self.nameBox.overwritingChanged.connect(self.updateButtons)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        # respond to intial validation
        self.okButton.setEnabled(self.nameBox.isValid())
        self.updateButtons(self.nameBox.overwritingName())
        
        self.resize(400,160) 
        
    def catalogHasChanged(self):
        catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspaces = catalog.get_workspaces()        
        self.workspaceBox.clear()        
        try:
            defaultWorkspace = catalog.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None                  
        workspaceNames = [w.name for w in self.workspaces]        
        self.workspaceBox.addItems(workspaceNames)
        if defaultName is not None:
            self.workspaceBox.setCurrentIndex(workspaceNames.index(defaultName))

        gslayers = [lyr.name for lyr in catalog.get_layers()]
        self.nameBox.setNames(gslayers)

    @QtCore.pyqtSlot(bool)
    def updateButtons(self, overwriting):
        txt = "Overwrite" if overwriting else "OK"
        self.okButton.setText(txt)
        self.okButton.setDefault(not overwriting)
        self.cancelButton.setDefault(overwriting)
    
    def okPressed(self):                
        self.catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspace = self.workspaces[self.workspaceBox.currentIndex()]
        self.layername = unicode(self.nameBox.definedName())
        self.close()

    def cancelPressed(self):
        self.catalog = None        
        self.workspace = None
        self.layername = None
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
        self.setWindowTitle('Publish layers')         
        self.table = QtGui.QTableWidget(None)
        
        columnCount = 1 if len(self.catalogs) == 1 else 2
        columns = ["Workspace"] if len(self.catalogs) == 1 else ["Catalog", "Workspace"]
        self.table.setColumnCount(columnCount)
        self.table.setColumnWidth(0,300)
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)            
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setTableContent()        

        layout.addWidget(self.table)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel) 
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        
    def setTableContent(self):
        showCatalogCol = len(self.catalogs) > 1        
        self.table.setRowCount(len(self.layers))
        layernames = [layer.name().ljust(25) for layer in self.layers]
        self.table.setVerticalHeaderLabels(layernames)        
        for idx, layer in enumerate(self.layers):
            if showCatalogCol:
                catalogBox = QtGui.QComboBox()                       
                catalogBox.addItems(self.catalogs.keys())
                catalogBox.currentIndexChanged.connect(lambda: self.catalogHasChanged(idx))
                self.table.setCellWidget(idx, 0, catalogBox)                            
            workspaceBox = QtGui.QComboBox()                                          
            cat = self.catalogs.values()[0]
            workspaces = cat.get_workspaces()            
            try:
                defaultWorkspace = cat.get_default_workspace()
                defaultWorkspace.fetch()
                defaultName = defaultWorkspace.dom.find('name').text
            except:
                defaultName = None  
            workspaceNames = [w.name for w in workspaces]        
            workspaceBox.addItems(workspaceNames)
            if defaultName is not None: 
                workspaceBox.setCurrentIndex(workspaceNames.index(defaultName))
            if showCatalogCol:            
                self.table.setCellWidget(idx, 1, workspaceBox)
            else:
                self.table.setCellWidget(idx, 0, workspaceBox)
    
    def catalogHasChanged(self, row):        
        catalogBox = self.table.cellWidget(row, 0)
        cat = self.catalogs[catalogBox.currentText()]
        try:
            defaultWorkspace = cat.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None  
        workspaces = cat.get_workspaces()        
        workspaceNames = [w.name for w in workspaces]        
        workspaceBox = self.table.cellWidget(row, 1)
        workspaceBox.clear()
        workspaceBox.addItems(workspaceNames)             
        if defaultName is not None:
            workspaceBox.setCurrentIndex(workspaceNames.index(defaultName)) 
    
    def okPressed(self):
        self.topublish = []        
        for idx, layer in enumerate(self.layers):
            if len(self.catalogs) > 1:
                catalogBox = self.table.cellWidget(idx, 0)
                catalog = self.catalogs[catalogBox.currentText()]
                workspaceBox = self.table.cellWidget(idx, 1)
                workspaces = catalog.get_workspaces()
                workspace = workspaces[workspaceBox.currentIndex()]
                self.topublish.append((layer, catalog, workspace))
            else:
                catalog = self.catalogs.values()[0]
                workspaceBox = self.table.cellWidget(idx, 0)
                workspaces = catalog.get_workspaces()
                workspace = workspaces[workspaceBox.currentIndex()]
                self.topublish.append((layer, catalog, workspace))
        self.close()

    def cancelPressed(self):
        self.topublish = None                
        self.close()             
        
