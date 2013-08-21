from PyQt4 import QtGui, QtCore
from opengeo.geoserver.catalog import Catalog


class DefineCatalogDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(DefineCatalogDialog, self).__init__(parent)
        self.catalog = None
        self.name = None
        self.initGui()
        
        
    def initGui(self):                         
        self.setWindowTitle('Catalog definition')
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Catalog name')
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('Default GeoServer catalog')
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)
        
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        urlLabel = QtGui.QLabel('URL')
        self.urlBox = QtGui.QLineEdit()
        settings = QtCore.QSettings()
        if settings.contains('/OpenGeo/LastCatalogUrl'):
            url = settings.value('/OpenGeo/LastCatalogUrl')
        else:
            url = 'http://localhost:8080/geoserver'                
        self.urlBox.setText(url)
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        self.usernameBox = QtGui.QLineEdit()
        self.usernameBox.setText('admin')
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QtGui.QLabel('Password')
        self.passwordBox = QtGui.QLineEdit()
        self.passwordBox.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.passwordBox.setText('geoserver')
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        layout.addLayout(horizontalLayout)
               
        
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)
            
    
    def getCatalog(self):        
        return self.catalog
    
    def getName(self):
        return self.name
    
    def okPressed(self):        
        self.catalog = Catalog(unicode(self.urlBox.text() + '/rest'), unicode(self.usernameBox.text()), unicode(self.passwordBox.text()))
        self.name = unicode(self.nameBox.text())
        settings = QtCore.QSettings()
        settings.setValue('/OpenGeo/LastCatalogUrl', self.urlBox.text())        
        self.close()

    def cancelPressed(self):
        self.catalog = None
        self.name = None
        self.close()  