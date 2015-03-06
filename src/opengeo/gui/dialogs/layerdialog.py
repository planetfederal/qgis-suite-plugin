from PyQt4 import QtGui, QtCore

from opengeo.qgis import layers
from opengeo.gui.gsnameutils import GSNameWidget, xmlNameFixUp, \
    xmlNameRegexMsg, xmlNameRegex

from functools import partial


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

    def __init__(self, catalogs, layers, overwrite=False, parent = None):
        super(PublishLayersDialog, self).__init__(parent)
        self.catalogs = catalogs        
        self.layers = layers
        self.overwrite = overwrite
        self.showCatalogCol = len(self.catalogs) > 1
        self.columns = []
        self.nameBoxes = []
        self.topublish = None
        self.lyr = "Layer"
        self.cat = "Catalog"
        self.wrksp = "Workspace"
        self.ow = "OW"
        self.name = "Name"
        self.initGui()
        
        
    def initGui(self):
        self.resize(760, 400)
        layout = QtGui.QVBoxLayout()                                               
        self.setWindowTitle('Publish layers')         
        self.table = QtGui.QTableWidget(None)

        self.columns = [self.lyr, self.cat, self.wrksp, self.ow, self.name] if self.showCatalogCol \
            else [self.lyr, self.wrksp, self.ow, self.name]

        self.table.setColumnCount(len(self.columns))
        self.table.horizontalHeader().setDefaultSectionSize(120)
        self.table.setColumnWidth(self.getColumn(self.lyr), 160)
        self.table.setColumnWidth(self.getColumn(self.wrksp), 160)
        self.table.setColumnWidth(self.getColumn(self.ow), 25)
        self.table.setColumnWidth(self.getColumn(self.name), 140)
        if self.showCatalogCol:
            self.table.setColumnWidth(self.getColumn(self.cat), 140)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setMinimumSectionSize(25)
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setTableContent()        

        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        layout.addWidget(self.table)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.validateNames()  # so OK button is initially updated

    def getColumn(self, name):
        if name not in self.columns:
            return None
        return self.columns.index(name)
        
    def setTableContent(self):
        self.table.setRowCount(len(self.layers))
        cat = self.catalogs.values()[0]
        catlayers = [lyr.name for lyr in cat.get_layers()]
        for idx, layer in enumerate(self.layers):

            lyritem = QtGui.QTableWidgetItem(layer.name())
            lyritem.setToolTip(layer.name())
            lyritem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.setItem(idx, self.getColumn("Layer"), lyritem)

            nameBox = GSNameWidget(
                name=xmlNameFixUp(layer.name()),
                nameregex=xmlNameRegex(),
                nameregexmsg=xmlNameRegexMsg(),
                names=catlayers,
                unique=not self.overwrite)
            self.table.setCellWidget(idx, self.getColumn(self.name), nameBox)

            self.nameBoxes.append(nameBox)

            overwriteBox = QtGui.QCheckBox()
            overwriteBox.setEnabled(False)
            overwriteBox.setToolTip("Overwrite existing layer")
            self.table.setCellWidget(idx, self.getColumn(self.ow), overwriteBox)

            nameBox.nameValidityChanged.connect(self.validateNames)
            nameBox.overwritingChanged[bool].connect(overwriteBox.setChecked)
            overwriteBox.setChecked(nameBox.overwritingName())  # initial update

            if self.showCatalogCol:
                catalogBox = QtGui.QComboBox()
                catalogBox.setSizePolicy(
                    QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                                      QtGui.QSizePolicy.Fixed))
                catalogBox.addItems(self.catalogs.keys())
                catalogBox.currentIndexChanged.connect(partial(self.catalogHasChanged, idx))
                self.table.setCellWidget(idx, self.getColumn(self.cat), catalogBox)

            workspaceBox = QtGui.QComboBox()
            workspaceBox.setSizePolicy(
                QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                                  QtGui.QSizePolicy.Fixed))
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
            self.table.setCellWidget(idx, self.getColumn(self.wrksp), workspaceBox)

    def catalogHasChanged(self, row):
        catalogBox = self.table.cellWidget(row, self.getColumn(self.cat))
        catname = unicode(catalogBox.currentText())
        cat = self.catalogs[catname]

        catlayers = [lyr.name for lyr in cat.get_layers()]
        nameBox = self.table.cellWidget(row, self.getColumn(self.name))
        nameBox.setNames(catlayers)

        try:
            defaultWorkspace = cat.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None  
        workspaces = cat.get_workspaces()        
        workspaceNames = [w.name for w in workspaces]        
        workspaceBox = self.table.cellWidget(row, self.getColumn(self.wrksp))
        workspaceBox.clear()
        workspaceBox.addItems(workspaceNames)             
        if defaultName is not None:
            workspaceBox.setCurrentIndex(workspaceNames.index(defaultName))

    def validateNames(self):
        valid = True
        for namebox in self.nameBoxes:
            if not namebox.isValid():
                valid = False
                break
        self.okButton.setEnabled(valid)

    def layersToPublish(self):
        topublish = []
        for idx, layer in enumerate(self.layers):
            nameBox = self.table.cellWidget(idx, self.getColumn(self.name))
            layername = nameBox.definedName()
            if self.showCatalogCol:
                catalogBox = self.table.cellWidget(idx, self.getColumn(self.cat))
                catalog = self.catalogs[catalogBox.currentText()]
                workspaceBox = self.table.cellWidget(idx, self.getColumn(self.wrksp))
                workspaces = catalog.get_workspaces()
                workspace = workspaces[workspaceBox.currentIndex()]
                topublish.append((layer, catalog, workspace, layername))
            else:
                catalog = self.catalogs.values()[0]
                workspaceBox = self.table.cellWidget(idx, self.getColumn(self.wrksp))
                workspaces = catalog.get_workspaces()
                workspace = workspaces[workspaceBox.currentIndex()]
                topublish.append((layer, catalog, workspace, layername))
        return topublish
    
    def okPressed(self):
        self.topublish = self.layersToPublish()
        self.close()

    def cancelPressed(self):
        self.topublish = None                
        self.close()
