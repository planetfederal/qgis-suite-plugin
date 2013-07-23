from PyQt4.QtCore import *
from qgis.core import *
from opengeo.gui.catalogdialog import DefineCatalogDialog
from opengeo.gui.explorerthread import ExplorerThread
from opengeo.gui.exploreritems import *

from opengeo.gui.explorertree import ExplorerTreeWidget

class GeoServerExplorer(QtGui.QDockWidget):
    
    def __init__(self, parent = None):
        super(GeoServerExplorer, self).__init__()        
        self.initGui()
        
    def initGui(self):    
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)  
        self.dockWidgetContents = QtGui.QWidget()
        self.setWindowTitle('GeoServer explorer')
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.verticalLayout = QtGui.QVBoxLayout(self.splitter)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)         
        self.tree = ExplorerTreeWidget(self)                                                                                             
        self.verticalLayout.addWidget(self.tree)         
        self.log = QtGui.QTextEdit(self.splitter) 
        self.progress = QtGui.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)                       
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setMargin(0)        
        self.layout.addWidget(self.splitter)
        self.layout.addWidget(self.progress)
        self.dockWidgetContents.setLayout(self.layout)
        self.setWidget(self.dockWidgetContents)       
    

    def updateContent(self):
        self.tree.updateContent()
            
    def run(self, command, okmsg, refresh, *params):
        error = False                                
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))        
        thread = ExplorerThread(command, *params)                
        def finish():
            QtGui.QApplication.restoreOverrideCursor()
            for item in refresh:
                item.refreshContent()
            self.setInfo(okmsg)
        def error(msg):
            QtGui.QApplication.restoreOverrideCursor()
            self.setInfo(msg, True)   
            error = True         
        thread.finish.connect(finish)
        thread.error.connect(error)                                         
        thread.start()
        thread.wait()
        return error
        
    def setInfo(self, msg, error = False):
        if error:
            self.log.append('<ul><li><span style="color:red">ERROR: ' + msg + '</span></li></ul>')
        else:
            self.log.append('<ul><li><span style="color:blue">INFO: ' + msg + '</span></li></ul>')
            
    