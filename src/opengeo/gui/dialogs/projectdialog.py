from PyQt4 import QtGui, QtCore
from opengeo.gui.gsnameutils import GSNameWidget, \
    xmlNameEmptyRegex, xmlNameRegexMsg

class PublishProjectDialog(QtGui.QDialog):
    
    def __init__(self, catalogs, parent = None):
        super(PublishProjectDialog, self).__init__(parent)
        self.catalogs = catalogs            
        self.catalog = None
        self.workspace = None
        self.groupName = None
        self.initGui()

    def initGui(self):
        layout = QtGui.QVBoxLayout()                                                
        self.setWindowTitle('Publish project')
                                 
        verticalLayout = QtGui.QVBoxLayout()        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        catalogLabel = QtGui.QLabel('Catalog')
        self.catalogBox = QtGui.QComboBox()        
        self.catalogBox.addItems(self.catalogs.keys())
        self.catalogBox.currentIndexChanged.connect(self.catalogHasChanged)
        horizontalLayout.addWidget(catalogLabel)
        horizontalLayout.addWidget(self.catalogBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        workspaceLabel = QtGui.QLabel('Workspace')
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
        horizontalLayout.addWidget(workspaceLabel)
        horizontalLayout.addWidget(self.workspaceBox)
        verticalLayout.addLayout(horizontalLayout)
        
        self.destGroupBox = QtGui.QGroupBox()
        self.destGroupBox.setLayout(verticalLayout)
        
        verticalLayout = QtGui.QVBoxLayout()
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        groupLabel = QtGui.QLabel('Global group name')
        groupnames = [grp.name for grp in cat.get_layergroups()]
        self.groupNameBox = GSNameWidget(
            nameregex=xmlNameEmptyRegex(),
            nameregexmsg=xmlNameRegexMsg(),
            names=groupnames,
            unique=True,
            allowempty=True)
        horizontalLayout.addWidget(groupLabel)
        horizontalLayout.addWidget(self.groupNameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        self.groupGroupBox = QtGui.QGroupBox()
        self.groupGroupBox.setLayout(verticalLayout)

        layout.addWidget(self.destGroupBox)
        layout.addWidget(self.groupGroupBox)

        overwriteLabel = QtGui.QLabel(
            "Ungrouped layers will be published first.\n"
            "No GeoServer items will be overwritten.")
        overwriteLabel.setAlignment(QtCore.Qt.AlignHCenter)
        f = overwriteLabel.font()
        f.setItalic(True)
        overwriteLabel.setFont(f)
        layout.addWidget(overwriteLabel)
        
        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Close)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.groupNameBox.nameValidityChanged.connect(self.validateGroupName)
        # set initial enabled state of Ok button
        self.validateGroupName()
        
        self.resize(400,200) 
        
    def catalogHasChanged(self):
        catalog = self.catalogs[self.catalogBox.currentText()]                        
        self.workspaces = catalog.get_workspaces()        
        try:
            defaultWorkspace = catalog.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None                  
        workspaceNames = [w.name for w in self.workspaces]
        self.workspaceBox.clear()        
        self.workspaceBox.addItems(workspaceNames)
        if defaultName is not None:
            self.workspaceBox.setCurrentIndex(workspaceNames.index(defaultName))

        groupnames = [grp.name for grp in catalog.get_layergroups()]
        self.groupNameBox.setNames(groupnames)

    @QtCore.pyqtSlot()
    def validateGroupName(self):
        self.okButton.setEnabled(self.groupNameBox.isValid())

    @QtCore.pyqtSlot()
    def okPressed(self):                
        self.catalog = self.catalogs[self.catalogBox.currentText()]
        self.workspace = self.workspaces[self.workspaceBox.currentIndex()]
        self.groupName = self.groupNameBox.definedName()
        if self.groupName.strip() == "":
            self.groupName = None
        self.close()

    @QtCore.pyqtSlot()
    def cancelPressed(self):
        self.catalog = None        
        self.workspace = None
        self.groupName = None
        self.close()
