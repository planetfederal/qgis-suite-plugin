from PyQt4 import QtGui, QtCore

class DefineWorkspaceDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(DefineWorkspaceDialog, self).__init__(parent)
        self.uri = None        
        self.name = None
        self.initGui()
        
        
    def initGui(self):     
        self.setWindowTitle('New workspace')                    
        verticalLayout = QtGui.QVBoxLayout()                                
                        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Workspace name')
        nameLabel.setMinimumWidth(150)
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('workspace_name')
        self.nameBox.setMinimumWidth(250)        
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        uriLabel = QtGui.QLabel('URI')
        uriLabel.setMinimumWidth(150)
        self.uriBox = QtGui.QLineEdit()
        self.uriBox.setText('')
        self.uriBox.setMinimumWidth(250)
        horizontalLayout.addWidget(uriLabel)
        horizontalLayout.addWidget(self.uriBox)
        verticalLayout.addLayout(horizontalLayout)
        
        self.groupBox = QtGui.QGroupBox()        
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox)   
        self.spacer = QtGui.QSpacerItem(20,20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(self.spacer)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)               
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
           
    def getWorkspace(self):        
        return self.workspace
    
    
    def okPressed(self):
        self.uri = unicode(self.uriBox.text())
        self.name = unicode(self.nameBox.text()) 
        self.close()

    def cancelPressed(self):
        self.uri = None
        self.name = None
        self.close()  