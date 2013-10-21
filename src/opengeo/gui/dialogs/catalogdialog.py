from PyQt4 import QtGui, QtCore

class DefineCatalogDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(DefineCatalogDialog, self).__init__(parent)
        self.ok = False
        self.initGui()
        
        
    def initGui(self):                         
        self.setWindowTitle('Catalog definition')
        
        verticalLayout = QtGui.QVBoxLayout()                                   
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Catalog name')
        nameLabel.setMinimumWidth(150)
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('Default GeoServer catalog')
        self.nameBox.setMinimumWidth(250)
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        urlLabel = QtGui.QLabel('URL')
        urlLabel.setMinimumWidth(150)
        self.urlBox = QtGui.QLineEdit()
        settings = QtCore.QSettings()        
        url = settings.value('/OpenGeo/LastCatalogUrl', 'http://localhost:8080/geoserver')                
        self.urlBox.setText(url)
        self.urlBox.setMinimumWidth(250)
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        usernameLabel.setMinimumWidth(150)
        self.usernameBox = QtGui.QLineEdit()
        self.usernameBox.setText('admin')
        self.usernameBox.setMinimumWidth(250)
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QtGui.QLabel('Password')
        passwordLabel.setMinimumWidth(150)
        self.passwordBox = QtGui.QLineEdit()
        self.passwordBox.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordBox.setText('geoserver')
        self.passwordBox.setMinimumWidth(250)
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        verticalLayout.addLayout(horizontalLayout)
        
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("GeoServer Connection parameters")
        self.groupBox.setLayout(verticalLayout)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox)  
        self.spacer = QtGui.QSpacerItem(20,20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(self.spacer)
        
        verticalLayout2 = QtGui.QVBoxLayout()
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        urlLabel = QtGui.QLabel('URL')
        urlLabel.setMinimumWidth(150)
        self.urlGeonodeBox = QtGui.QLineEdit()        
        geonodeUrl = settings.value('/OpenGeo/LastGeonodeUrl', 'http://localhost:8000/')                
        self.urlGeonodeBox.setText(geonodeUrl)
        self.urlGeonodeBox.setMinimumWidth(250)
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlGeonodeBox)
        verticalLayout2.addLayout(horizontalLayout)

        self.geonodeBox = QtGui.QGroupBox()
        self.geonodeBox.setTitle("GeoNode Connection parameters (Optional)")
        self.geonodeBox.setLayout(verticalLayout2)

        layout.addWidget(self.geonodeBox)  
        self.spacer = QtGui.QSpacerItem(20,20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(self.spacer)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,200)
            
       
    def okPressed(self):        
        self.url = unicode(self.urlBox.text() + '/rest')
        self.username = unicode(self.usernameBox.text())
        self.password = unicode(self.passwordBox.text())
        self.name = unicode(self.nameBox.text())
        self.geonodeUrl = unicode(self.urlGeonodeBox.text())
        settings = QtCore.QSettings()
        settings.setValue('/OpenGeo/LastCatalogUrl', self.urlBox.text())
        settings.setValue('/OpenGeo/LastGeoNodeUrl', self.urlGeonodeBox.text()) 
        saveCatalogs = bool(settings.value("/OpenGeo/Settings/GeoServer/SaveCatalogs", True, bool))
        if saveCatalogs:  
            settings.beginGroup("/OpenGeo/GeoServer/" + self.name)                                                                
            settings.setValue("url", self.url);                
            settings.setValue("username", self.username);
            settings.setValue("password", self.password);
            settings.setValue("geonode", self.geonodeUrl);        
            settings.endGroup()
        self.ok = True       
        self.close()

    def cancelPressed(self):
        self.ok = False        
        self.close()  