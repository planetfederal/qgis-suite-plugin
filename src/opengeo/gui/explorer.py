import os
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *
from opengeo.gui.exploreritems import *
from opengeo.gui.explorerwidget import ExplorerWidget
from opengeo import config
from raven import Client
from qgis.utils import pluginMetadata
import traceback


SENTRY_URL = "http://5d60c883c47645b78effecd67e0f9c73:a11d69b72e5b439fb30ec4c4bc0d42bb@sentry.boundlessgeo.com/2"


class OpenGeoExplorer(QtGui.QDockWidget):

    def __init__(self, parent = None, singletab = True):
        super(OpenGeoExplorer, self).__init__()  
        self.singletab = singletab
        dsn = QSettings().value("/OpenGeo/Settings/General/SentryUrl", "")
        dsn = dsn if (dsn != NULL and dsn.strip()) != "" else SENTRY_URL 
        context = {'sys.argv': []}        
        try:
            self.ravenClient = Client(dsn=dsn, context = context)
        except:
            self.ravenClient = Client(dsn=SENTRY_URL, context = context)
        self.initGui()
        
    def initGui(self):
        self.explorerWidget = None 
        self.progressMaximum = 0   
        self.isProgressVisible = False
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)  
        self.dockWidgetContents = QtGui.QWidget()
        self.setWindowTitle('OpenGeo explorer')
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.subwidget = QtGui.QWidget()               
        self.explorerWidget = ExplorerWidget(self, self.singletab)
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolbar.setVisible(self.singletab)
        self.setToolbarActions([])
        self.splitter.addWidget(self.explorerWidget)                             
        self.log = QtGui.QTextEdit()        
        self.description = QtGui.QWidget()
        self.descriptionLayout = QtGui.QVBoxLayout()
        self.descriptionLayout.setSpacing(2)
        self.descriptionLayout.setMargin(0)
        self.description.setLayout(self.descriptionLayout)        
        self.splitter.addWidget(self.description)
        self.setDescriptionWidget()
        showDescription = QSettings().value("/OpenGeo/Settings/General/ShowDescription", True, bool)  
        self.description.setVisible(showDescription)
        self.progress = None
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setMargin(0)                                               
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.splitter)     
        self.setLayout(self.layout)
        self.dockWidgetContents.setLayout(self.layout)
        self.setWidget(self.dockWidgetContents)  
        
        self.topLevelChanged.connect(self.dockStateChanged)
        
    def dockStateChanged(self, floating):        
        if floating:
            self.resize(800, 450)            
            self.splitter.setOrientation(Qt.Horizontal)
        else:
            self.splitter.setOrientation(Qt.Vertical)                

    def setToolbarActions(self, actions):                
        self.toolbar.clear()
        for action in actions:
            if action.icon().isNull():
                icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/process.png")
                action.setIcon(icon)        
        if len(actions) == 0:
            refreshIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/refresh.png")                         
            refreshAction = QtGui.QAction(refreshIcon, "Refresh", self)
            refreshAction.triggered.connect(self.explorerWidget.refreshContent)
            actions.append(refreshAction)
             
        for action in actions:   
            button = QtGui.QPushButton()
            button.setIcon(action.icon())
            button.setToolTip(action.text())
            button.setEnabled(action.isEnabled())
            button.clicked.connect(action.trigger)                           
            self.toolbar.addWidget(button)
            
        self.toolbar.update()
                    
    def refreshContent(self):
        showDescription = QSettings().value("/OpenGeo/Settings/General/ShowDescription", True, bool)  
        self.description.setVisible(showDescription)
        self.explorerWidget.refreshContent()
        self.refreshDescription()
        
    def catalogs(self):        
        if self.explorerWidget is None:
            return {}
        return self.explorerWidget.catalogs()
    
    def pgDatabases(self):
        return self.explorerWidget.pgDatabases()
        
    def updateQgisContent(self):
        self.explorerWidget.updateQgisContent()
                   
    def run(self, command, msg, refresh, *params):
        noerror = True
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        try:
            command(*params)            
            for item in refresh:
                if item is not None:
                    item.refreshContent(self)
            if None in refresh:
                self.refreshContent()                        
            if msg is not None and not self.isProgressVisible:
                self.setInfo("Operation <i>" + msg + "</i> correctly executed")                    
        except Exception, e:                                
            self.setError(unicode(e.message, errors = "ignore").encode("utf-8") + "\n" + traceback.format_exc())
            noerror = False
        finally:
            QtGui.QApplication.restoreOverrideCursor()
            self.refreshDescription()
                               
        return noerror
            
    def resetActivity(self):   
        if self.progress is not None:            
            config.iface.messageBar().clearWidgets()
            self.isProgressVisible = False
            self.progress = None  
            self.progressMaximum = 0                    
        
    def setProgress(self, value):
        if self.progress is not None:
            self.progress.setValue(value)        
        
    def setProgressMaximum(self, value, msg = ""):
        self.progressMaximum = value
        self.isProgressVisible = True
        self.progressMessageBar = config.iface.messageBar().createMessage(msg)
        self.progress = QtGui.QProgressBar()
        self.progress.setMaximum(self.progressMaximum)
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.progressMessageBar.layout().addWidget(self.progress) 
        config.iface.messageBar().pushWidget(self.progressMessageBar, QgsMessageBar.INFO)   

    def setInfo(self, msg):
        config.iface.messageBar().pushMessage("Info", msg,
                                              level = QgsMessageBar.INFO,
                                              duration = 3)

    def setWarning(self, msg):
        config.iface.messageBar().pushMessage("Warning", msg,
                                              level = QgsMessageBar.WARNING,
                                              duration = 15)

    def setError(self, msg):
        firstLine = msg.split("\n")[0]
        if self.progressMaximum != 0:
            QtGui.QMessageBox.critical(self, "Error", firstLine)
        widget = config.iface.messageBar().createMessage("Error", firstLine)
        sendButton = QtGui.QPushButton(widget)
        sendButton.setText("Report error")
        showButton = QtGui.QPushButton(widget)
        showButton.setText("View more")
        def reportError():
            version = "Plugin version: " + pluginMetadata("opengeo", "version")
            message = unicode(msg, errors = "ignore") + "\n" + version
            self.ravenClient.captureMessage(message)
            self.resetActivity()
        def showMore():
            dlg = QgsMessageOutput.createMessageOutput()
            dlg.setTitle('Error')
            dlg.setMessage(msg, QgsMessageOutput.MessageHtml)
            dlg.showMessage()
        sendButton.pressed.connect(reportError)
        showButton.pressed.connect(showMore)
        widget.layout().addWidget(sendButton)
        widget.layout().addWidget(showButton)
        config.iface.messageBar().pushWidget(widget, QgsMessageBar.CRITICAL,
                                             duration = 15)

    def setDescriptionWidget(self, widget = None):                
        item = self.descriptionLayout.itemAt(0)        
        if item:
            self.descriptionLayout.removeItem(item)
            item.widget().close()
        if widget is None:                    
            widget = QtGui.QTextBrowser()
            widget.setHtml(u'<div style="background-color:#ffffcc;"><h1>No description available</h1></div><ul>') 
                                  
        self.descriptionLayout.addWidget(widget)
        
        

    def refreshDescription(self):
        item = self.explorerWidget.currentTree().lastClickedItem()
        if item is not None:
            try:      
                self.explorerWidget.currentTree().treeItemClicked(item, 0)
            except:
                self.setDescriptionWidget(None)        
    