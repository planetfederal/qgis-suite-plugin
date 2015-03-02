from PyQt4 import QtGui, QtCore

class UserPasswdDialog(QtGui.QDialog):
    
    def __init__(self, user=None, passwd=None, parent=None):
        super(UserPasswdDialog, self).__init__(parent)
        self.user = user
        self.passwd = passwd
        self.initGui()        
        
    def initGui(self):                         
        self.setWindowTitle('Database credentials')
        verticalLayout = QtGui.QVBoxLayout()                                            
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        usernameLabel.setMaximumWidth(100)
        usernameLabel.setMinimumWidth(100)
        self.usernameBox = QtGui.QLineEdit()
        self.usernameBox.setText(self.user if self.user is not None else '')
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QtGui.QLabel('Password')
        passwordLabel.setMaximumWidth(100)
        passwordLabel.setMinimumWidth(100)
        self.passwordBox = QtGui.QLineEdit()
        self.passwordBox.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordBox.setText(self.passwd if self.passwd is not None else '')
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        verticalLayout.addLayout(horizontalLayout)
               
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("user/password")
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox) 
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)
          
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,200)
            
    
    def okPressed(self):
        self.user = unicode(self.usernameBox.text())
        self.passwd = unicode(self.passwordBox.text()) 
        self.close()

    def cancelPressed(self):
        self.user = None
        self.passwd = None
        self.close()  
