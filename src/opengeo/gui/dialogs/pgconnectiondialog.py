from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from opengeo.postgis.connection import PgConnection

class NewPgConnectionDialog(QDialog):
    
    def __init__(self, parent = None, conn = None):
        QDialog.__init__(self, parent)           
        self._conn = conn
        self.conn = None              
        self.setupUi()

    def setupUi(self):             
        self.setWindowTitle('Create new PostGIS connection')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        settings = QSettings()
        
        self.layout = QVBoxLayout()        
        
        self.groupBox = QGroupBox()
        self.groupBox.setTitle("Connection parameters")
        self.verticalLayout = QVBoxLayout()
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QLabel('Name')
        nameLabel.setMinimumWidth(150)
        self.nameBox = QLineEdit()  
        self.nameBox.setText("New PostGIS connection")  
        self.nameBox.setMinimumWidth(250)    
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        hostLabel = QLabel('Host')
        hostLabel.setMinimumWidth(150)
        self.hostBox = QLineEdit() 
        self.hostBox.setText(settings.value('/OpenGeo/PostGIS/LastHost', 'localhost'))
        self.hostBox.setMinimumWidth(250)                 
        horizontalLayout.addWidget(hostLabel)
        horizontalLayout.addWidget(self.hostBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        portLabel = QLabel('Port')
        portLabel.setMinimumWidth(150)
        self.portBox = QLineEdit()            
        self.portBox.setText(str(settings.value('/OpenGeo/PostGIS/LastPort', '54321')))
        self.portBox.setMinimumWidth(250)   
        horizontalLayout.addWidget(portLabel)
        horizontalLayout.addWidget(self.portBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        databaseLabel = QLabel('Database')
        databaseLabel.setMinimumWidth(150)        
        self.databaseBox = QLineEdit()    
        self.databaseBox.setText(settings.value('/OpenGeo/PostGIS/LastDatabase', ''))
        self.databaseBox.setMinimumWidth(250)      
        horizontalLayout.addWidget(databaseLabel)
        horizontalLayout.addWidget(self.databaseBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QLabel('User name')
        usernameLabel.setMinimumWidth(150)
        self.usernameBox = QLineEdit()   
        self.usernameBox.setText(settings.value('/OpenGeo/PostGIS/LastUserName', 'postgres'))
        self.usernameBox.setMinimumWidth(250)          
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QLabel('Password')
        passwordLabel.setMinimumWidth(150)
        self.passwordBox = QLineEdit() 
        self.passwordBox.setEchoMode(QLineEdit.Password)
        self.passwordBox.setMinimumWidth(250)       
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        self.groupBox.setLayout(self.verticalLayout)
        self.layout.addWidget(self.groupBox)   
        self.spacer = QSpacerItem(20,20, QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layout.addWidget(self.buttonBox)                
        
        self.setLayout(self.layout)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        
        if self._conn is not None:
            self.nameBox.setText(self._conn.name)
            self.hostBox.setText(str(self._conn.host))
            self.portBox.setText(str(self._conn.port))
            self.databaseBox.setText(self._conn.database)
            if self._conn.isValid:
                self.passwordBox.setText(self._conn.geodb.passwd)
                self.usernameBox.setText(self._conn.geodb.user)
            
    
    
    def accept(self):           
        if self.nameBox.text().strip() == "":
            self.nameBox.text.setStyleSheet("QLineEdit{background: yellow}")
            return
        if self.databaseBox.text().strip() == "":
            self.databaseBox.text.setStyleSheet("QLineEdit{background: yellow}")
            return
        if self.hostBox.text().strip() == "":
            self.hostBox.text.setStyleSheet("QLineEdit{background: yellow}")
            return
        try:
            int(self.portBox.text())
        except:
            self.portBox.text.setStyleSheet("QLineEdit{background: yellow}")                 
        settings = QSettings();
        settings.beginGroup("/PostgreSQL/connections/" + self.nameBox.text())                                                                
        settings.setValue("host", self.hostBox.text());
        settings.setValue("port", self.portBox.text());
        settings.setValue("database", self.databaseBox.text() );
        settings.setValue("username", self.usernameBox.text());
        settings.setValue("password", self.passwordBox.text());
        self.conn = PgConnection(self.nameBox.text(), settings.value('host'), int(settings.value('port')), 
                            settings.value('database'), settings.value('username'), 
                            settings.value('password'))
        settings.endGroup()
        settings.beginGroup("/OpenGeo/PostGIS") 
        settings.setValue("LastHost", self.hostBox.text());
        settings.setValue("LastPort", self.portBox.text());
        settings.setValue("LastDatabase", self.databaseBox.text() );
        settings.setValue("LastUserName", self.usernameBox.text());
        settings.endGroup()
        
        #delete the previous conenction if it has been renamed
        if self._conn is not None and self.conn.name == self._conn.name: 
            settings.beginGroup("/PostgreSQL/connections/" + self._conn.name) 
            settings.remove(""); 
            settings.endGroup();
        
        QDialog.accept(self)        
        
    def reject(self):
        self.conn = None    
        QDialog.reject(self)

        
        
       