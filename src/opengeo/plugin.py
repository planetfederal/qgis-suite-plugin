# -*- coding: utf-8 -*-

import os, sys
import inspect
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from qgis.core import *
from opengeo import config
from opengeo.gui.explorer import GeoServerExplorer
from opengeo.qgis import catalog

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class OpenGeoPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
        
    def unload(self):
        self.menu.deleteLater()

    def initGui(self):
        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("OpenGeo")
        
        self.explorer = GeoServerExplorer()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        self.explorer.hide()        

        icon = QIcon(os.path.dirname(__file__) + "/images/geoserver.png")
        self.explorerAction = QAction(icon, "GeoServer Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.menu.addAction(self.explorerAction)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)
        
    def openExplorer(self):
        self.explorer.updateContent()
        self.explorer.show()        
