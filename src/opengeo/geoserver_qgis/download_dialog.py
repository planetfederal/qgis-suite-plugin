"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer

Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from PyQt4 import QtCore, QtGui
from PyQt4 import Qt
from download_dialog_ui import Ui_DownloadDialog

from storage.qgscatalog import QGSCatalog
from qgslayermodel import QGSLayerModel


class DownloadDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_DownloadDialog()
        self.ui.setupUi(self)

        self.iface = iface

        #Set up the server connection parameter text boxes.
        self.txtServerUrl = self.ui.leServerUrl
        self.txtServerUrl.setText("http://localhost:8080/geoserver/rest")
        self.txtUsername = self.ui.leUsername
        self.txtUsername.setText("admin")
        self.txtPassword = self.ui.lePassword
        self.txtPassword.setText("geoserver")
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)

        myButton = self.ui.pbnConnect
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.populateTableView)

        #Set up the table view
        #TODO: use a tree view that is folded on the workspace names
        self.tableView = self.ui.layerTreeView
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #Set up the button
        myButton = self.ui.pbnDownload
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.downloadSelectedLayers)

        myButton = self.ui.pbnDownloadAdd
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.downloadAddLayers)

    def resizeColumns(self):
        for column in range(4):
            self.tableView.resizeColumnToContents(column)

    def populateTableView(self):
        serverUrl = unicode(self.txtServerUrl.text())
        username = unicode(self.txtUsername.text())
        password = unicode(self.txtPassword.text())

        qgs_cat = QGSCatalog(serverUrl, username=username, password=password)
        # QtCore.pyqtRemoveInputHook()
        # import pdb; pdb.set_trace()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Loading the layer list", "Cancel", 0, 0, self.tableView)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.resize(400, 110)
        progress.setWindowTitle("Loading")
        progress.show()

        self.all_layers = qgs_cat.get_layers_from_capabilities()

        QtGui.QApplication.restoreOverrideCursor()
        progress.hide()

        self.model = QGSLayerModel(self.all_layers)

        self.tableView.setModel(self.model)
        self.tableView.setSortingEnabled(True)
        self.resizeColumns()

    def downloadSelectedLayers(self):
        downloaded_layers = []
        selected_indexes = self.tableView.selectionModel().selection().indexes()

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtGui.QProgressDialog("Downloading the selected layer list", "Cancel", 0, 0, self.tableView)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.resize(400, 110)
        progress.setWindowTitle("Loading")
        progress.show()

        for index in selected_indexes:
            if index.column() != QGSLayerModel.NAME:
                continue
            selected_layer_name = unicode(index.data().toString())
            selected_layer = self.all_layers[selected_layer_name]
            selected_layer.download()
            downloaded_layers.append(selected_layer)

        QtGui.QApplication.restoreOverrideCursor()
        progress.hide()

        return downloaded_layers

    def AddLayers(self, layer_list):
        for layer in layer_list:
            layer_type = layer.resource.resource_type
            if layer_type == "featureType":
                self.iface.addVectorLayer(layer.file_paths['data'], layer.name, "ogr")
            elif layer_type == "coverage":
                self.iface.addRasterLayer(layer.file_paths['data'], "raster")

    def downloadAddLayers(self):
        downloaded_layers = self.downloadSelectedLayers()
        self.AddLayers(downloaded_layers)
