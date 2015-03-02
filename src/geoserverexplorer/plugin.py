# -*- coding: utf-8 -*-

import os
import webbrowser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import config
from geoserverexplorer.gui.explorer import GeoServerExplorer
from geoserverexplorer.gui.dialogs.configdialog import ConfigDialog
from geoserverexplorer.geoserver import pem

class GeoServerExplorerPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface

    def unload(self):
        pem.removePkiTempFiles(self.explorer.catalogs())
        self.explorer.deleteLater()

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/images/geoserver.png")
        self.explorerAction = QAction(icon, "GeoServer Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.iface.addPluginToWebMenu(u"GeoServer", self.explorerAction)

        settings = QSettings()
        self.explorer = GeoServerExplorer()
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        if not settings.value("/GeoServer/Settings/General/ExplorerVisible", False, bool):
            self.explorer.hide()
        self.explorer.visibilityChanged.connect(self._explorerVisibilityChanged)


        icon = QIcon(os.path.dirname(__file__) + "/images/config.png")
        self.configAction = QAction(icon, "GeoServer Explorer settings", self.iface.mainWindow())
        self.configAction.triggered.connect(self.openSettings)
        self.iface.addPluginToWebMenu(u"GeoServer", self.configAction)

        icon = QIcon(os.path.dirname(__file__) + "/images/help.png")
        self.helpAction = QAction(icon, "GeoServer Explorer help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.showHelp)
        self.iface.addPluginToWebMenu(u"GeoServer", self.helpAction)

    def _explorerVisibilityChanged(self, visible):
        settings = QSettings()
        settings.setValue("/GeoServer/Settings/General/ExplorerVisible", visible)

    def showHelp(self):
        HELP_URL = "http://qgis.boundlessgeo.com/static/docs/index.html"
        webbrowser.open(HELP_URL)

    def openExplorer(self):
        self.explorer.show()

    def openSettings(self):
        dlg = ConfigDialog(self.explorer)
        dlg.exec_()
