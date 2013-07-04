"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer

This script initializes the plugin, making it known to QGIS.


Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import (QObject,
                          QFileInfo,
                          QTranslator,
                          SIGNAL,
                          QCoreApplication,
                          QSettings)
from PyQt4.QtGui import QAction, QIcon
import resources
from qgis.core import *

# Import the code for the dialog
from download_dialog import DownloadDialog
from upload_dialog import UploadDialog


class Plugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/geoserver_bridge"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/geoserverqgis_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        #------------------------------------
        # Create action for Download dialog
        #------------------------------------
        self.actionDownloadDialog = QAction(
            QIcon(":/plugins/geoserver_bridge/download_icon.png"),
            u"Geoserver Bridge Download", self.iface.mainWindow())

        QObject.connect(self.actionDownloadDialog, SIGNAL("triggered()"), self.showDownloadDialog)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionDownloadDialog)
        self.iface.addPluginToMenu(u"&Geoserver QGIS Bridge", self.actionDownloadDialog)

        #------------------------------------
        # Create action for Upload dialog
        #------------------------------------
        self.actionUploadDialog = QAction(
            QIcon(":/plugins/geoserver_bridge/upload_icon.png"),
            u"Geoserver Bridge Upload", self.iface.mainWindow())

        QObject.connect(self.actionUploadDialog, SIGNAL("triggered()"), self.showUploadDialog)

        self.iface.addToolBarIcon(self.actionUploadDialog)
        self.iface.addPluginToMenu(u"&Geoserver QGIS Bridge", self.actionUploadDialog)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Geoserver QGIS Bridge", self.actionDownloadDialog)
        self.iface.removePluginMenu(u"&Geoserver QGIS Bridge", self.actionUploadDialog)
        self.iface.removeToolBarIcon(self.actionDownloadDialog)
        self.iface.removeToolBarIcon(self.actionUploadDialog)

    def showDownloadDialog(self):
        self.download_dialog = DownloadDialog(self.iface)
        # show the dialog
        self.download_dialog.show()

    def showUploadDialog(self):
        self.upload_dialog = UploadDialog(self.iface)
        # show the dialog
        self.upload_dialog.show()
