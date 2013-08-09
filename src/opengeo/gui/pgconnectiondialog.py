from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from opengeo.postgis.connection import PgConnection

class NewPgConnectionDialog(QDialog):
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)    
        self.conn = None              
        self.setupUi()

    def setupUi(self):
        self.resize(400, 300)
        self.setWindowTitle('Create new PostGIS connection')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        self.layout = QVBoxLayout()        
        
        self.groupBox = QGroupBox()
        self.groupBox.setTitle("Connection parameters")
        self.verticalLayout = QVBoxLayout()
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QLabel('Name')
        self.nameBox = QLineEdit()        
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        hostLabel = QLabel('Host')
        self.hostBox = QLineEdit() 
        self.hostBox.setText("localhost")       
        horizontalLayout.addWidget(hostLabel)
        horizontalLayout.addWidget(self.hostBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        portLabel = QLabel('Port')
        self.portBox = QLineEdit()    
        self.portBox.setText("5432")    
        horizontalLayout.addWidget(portLabel)
        horizontalLayout.addWidget(self.portBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        databaseLabel = QLabel('Database')
        self.databaseBox = QLineEdit()        
        horizontalLayout.addWidget(databaseLabel)
        horizontalLayout.addWidget(self.databaseBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QLabel('User name')
        self.usernameBox = QLineEdit()            
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QLabel('Password')
        self.passwordBox = QLineEdit()        
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        self.verticalLayout.addLayout(horizontalLayout)
        
        self.groupBox.setLayout(self.verticalLayout)
        self.layout.addWidget(self.groupBox)   
        self.spacer = QSpacerItem(20,40, QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout.addItem(self.spacer)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layout.addWidget(self.buttonBox)                
        
        self.setLayout(self.layout)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
    
    
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
        
        QDialog.accept(self)        
        
    def reject(self):
        self.conn = None    
        QDialog.reject(self)

        
        
       