# -*- coding: utf-8 -*-

import os, sys
import inspect
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo import config
from opengeo.gui.explorer import OpenGeoExplorer

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class OpenGeoPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
        
    def unload(self):
        self.menu.deleteLater()
        self.iface.legendInterface().itemAdded.disconnect(self.explorer.updateContent)
        self.iface.legendInterface().itemRemoved.disconnect(self.explorer.updateContent)

    def initGui(self):
        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("OpenGeo")
        
        self.explorer = OpenGeoExplorer()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        self.explorer.hide()        

        icon = QIcon(os.path.dirname(__file__) + "/images/opengeo.png")
        self.explorerAction = QAction(icon, "OpenGeo Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.menu.addAction(self.explorerAction)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)
        
        self.iface.legendInterface().itemAdded.connect(self.explorer.updateContent)
        self.iface.legendInterface().itemRemoved.connect(self.explorer.updateContent)
        
    def openExplorer(self):
        self.explorer.updateContent()
        self.explorer.show()        
