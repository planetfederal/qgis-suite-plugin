from PyQt4 import QtGui, QtCore

class DefineWorkspaceDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(DefineWorkspaceDialog, self).__init__(parent)
        self.uri = None        
        self.name = None
        self.initGui()
        
        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Workspace name')
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('workspace_name')
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        uriLabel = QtGui.QLabel('URI')
        self.uriBox = QtGui.QLineEdit()
        self.uriBox.setText('')
        horizontalLayout.addWidget(uriLabel)
        horizontalLayout.addWidget(self.uriBox)
        layout.addLayout(horizontalLayout)
               
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)            
    
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