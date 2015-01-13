# -*- coding: utf-8 -*-

import os
import webbrowser
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo import config
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.dialogs.configdialog import ConfigDialog
from opengeo.geoserver import pem

class OpenGeoPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface

    def unload(self):
        self.menu.deleteLater()
        self.iface.legendInterface().itemAdded.disconnect(self.explorer.updateQgisContent)
        self.iface.legendInterface().itemRemoved.disconnect(self.explorer.updateQgisContent)
        pem.removePkiTempFiles(self.explorer.catalogs())
        self.explorer.deleteLater()

    def initGui(self):
        actions = self.iface.mainWindow().menuBar().actions()

        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("OpenGeo")
        for action in actions:
            if action.text() == 'OpenGeo':
                self.menu = action.menu()
                break

        icon = QIcon(os.path.dirname(__file__) + "/images/opengeo.png")
        self.explorerAction = QAction(icon, "OpenGeo Explorer", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.menu.addAction(self.explorerAction)

        settings = QSettings()
        singletab = settings.value("/OpenGeo/Settings/General/SingleTabUI", True, bool)
        self.explorer = OpenGeoExplorer(singletab = singletab)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)
        self.iface.legendInterface().itemAdded.connect(self.explorer.updateQgisContent)
        self.iface.legendInterface().itemRemoved.connect(self.explorer.updateQgisContent)
        if not settings.value("/OpenGeo/Settings/General/ExplorerVisible", False, bool):
            self.explorer.hide()
        self.explorer.visibilityChanged.connect(self._explorerVisiblityChanged)

        icon = QIcon(os.path.dirname(__file__) + "/images/config.png")
        self.configAction = QAction(icon, "OpenGeo Explorer settings", self.iface.mainWindow())
        self.configAction.triggered.connect(self.openSettings)
        self.menu.addAction(self.configAction)

        icon = QIcon(os.path.dirname(__file__) + "/images/help.png")
        self.helpAction = QAction(icon, "OpenGeo Explorer help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.showHelp)
        self.menu.addAction(self.helpAction)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)

    def _explorerVisiblityChanged(self, visible):
        settings = QSettings()
        settings.setValue("/OpenGeo/Settings/General/ExplorerVisible", visible)

    def showHelp(self):
        HELP_URL = "http://qgis.boundlessgeo.com/static/docs/index.html"
        webbrowser.open(HELP_URL)

    def openExplorer(self):
        self.explorer.updateQgisContent()
        self.explorer.show()

    def openSettings(self):
        dlg = ConfigDialog(self.explorer)
        dlg.exec_()
