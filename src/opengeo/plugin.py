# -*- coding: utf-8 -*-

import os, sys
import inspect
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo import config
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.dialogs.configdialog import ConfigDialog

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe()))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class OpenGeoPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
                
    def unload(self):
        self.menu.deleteLater()                
        self.iface.legendInterface().itemAdded.disconnect(self.explorer.updateQgisContent)
        self.iface.legendInterface().itemRemoved.disconnect(self.explorer.updateQgisContent)

    def initGui(self):
        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("OpenGeo")
        
        icon = QIcon(os.path.dirname(__file__) + "/images/opengeo.png")
        self.explorerAction = QAction(icon, "OpenGeo Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.menu.addAction(self.explorerAction)
        
        icon = QIcon(os.path.dirname(__file__) + "/images/config.png")
        self.configAction = QAction(icon, "Settings", self.iface.mainWindow())
        self.configAction.triggered.connect(self.openSettings)
        self.menu.addAction(self.configAction)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)
                
        settings = QSettings()
        singletab = settings.value("/OpenGeo/Settings/General/SingleTabUI", True, bool)        
        self.explorer = OpenGeoExplorer(singletab = singletab)        
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        self.iface.legendInterface().itemAdded.connect(self.explorer.updateQgisContent)
        self.iface.legendInterface().itemRemoved.connect(self.explorer.updateQgisContent)
        self.explorer.hide()         
        
    def openExplorer(self):
        self.explorer.updateQgisContent()
        self.explorer.show()   
        
    def openSettings(self):
        dlg = ConfigDialog()
        dlg.exec_()     
