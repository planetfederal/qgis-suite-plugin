"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer

Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from PyQt4 import (QtCore,
                   QtGui)
from PyQt4.Qt import *

import requests
from lxml import etree

from upload_dialog_ui import Ui_UploadDialog

from storage.qgscatalog import QGSCatalog
from storage.utilities import upload_layer_to_gs


from projectlayermodel import ProjectLayerModel


class UploadDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_UploadDialog()
        self.ui.setupUi(self)

        self.iface = iface

        myButton = self.ui.pbnUpload
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.uploadSelectedLayer)

        #Set up the table view
        self.layer_list = self.getProjectLayers()
        #self.model = ProjectLayerModel(layer_list)

        #self.tableView = self.ui.layerTableView
        #self.tableView.setModel(self.model)
        #self.resizeColumns()
        #self.tableView.setSortingEnabled(True)

        self.tableWidget = self.ui.layerTableWidget
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.populateLayerTable()

    def populateLayerTable(self):
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(self.layer_list))
        headers = ["Title", "Abstract", "Keywords", "GS Name", "Workspace"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row, layer in enumerate(self.layer_list):
            self.tableWidget.setItem(row, 0, QtGui.QTableWidgetItem(layer['title']))
            self.tableWidget.setItem(row, 1, QtGui.QTableWidgetItem(layer['abstract']))
            self.tableWidget.setItem(row, 2, QtGui.QTableWidgetItem(layer['keywords']))
            self.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem(layer['name']))
            combobox = self.createWorkspaceCombobox()
            self.tableWidget.setCellWidget(row, 4, combobox)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()

    # def resizeColumns(self):
    #     for column in range(3):
    #         self.tableView.resizeColumnToContents(column)

    def createWorkspaceCombobox(self):
        # Retrieve existing workspaces and fill a combox to give option to the users
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")
        all_workspaces = qgs_cat.get_workspaces()
        all_workspaces = [workspace.name for workspace in all_workspaces]
        # Retrieve default workspace name
        req = requests.get(qgs_cat.get_default_workspace().href, auth=('admin', 'geoserver'))
        doc = etree.fromstring(req.content)
        default_name = doc.find('name')
        default_name = default_name.text if not None else None
        # Create and fill ComboBox
        combobox = QtGui.QComboBox()
        selected_index = -1
        for workspace in all_workspaces:
            if workspace == default_name and workspace is not None:
                combobox.addItem(workspace + " [default]")
                selected_index = combobox.findText(workspace + " [default]")
            else:
                combobox.addItem(workspace)
        if selected_index != -1:
            combobox.setCurrentIndex(selected_index)
        return combobox

    def uploadSelectedLayer(self):
        uploaded_layers = []
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")

        selected_indexes = self.tableWidget.selectionModel().selectedRows()

        for row_index in selected_indexes:
            # from PyQt4.QtCore import pyqtRemoveInputHook; pyqtRemoveInputHook()
            # import pdb; pdb.set_trace()
 
            selected_layer_name = self.tableWidget.item(row_index.row(), 0).text()
            #Shouldn't require a loop but I didn't find a way to access directly a layer by id or by name
            for lyr in self.iface.mapCanvas().layers():
                if str(lyr.name()) == selected_layer_name:
                    file_path = QtCore.QFileInfo(lyr.dataProvider().dataSourceUri().section('|', 0, 0))

            workspace = self.tableWidget.cellWidget(row_index.row(), 4).currentText()
            if '[default]' in workspace:
                workspace = 'default'
            #TODO: support other sources of data (PostGIS...)
            upload_layer_to_gs(qgs_cat, str(selected_layer_name), str(file_path.absoluteFilePath()), workspace=str(workspace))
        return uploaded_layers

    def getProjectLayers(self):
        canvas = self.iface.mapCanvas()
        all_layers = canvas.layers()
        layer_list = []

        for layer in all_layers:
            layer_list.append({
                'title': str(layer.name()),
                'name': '',
                'abstract': '',
                'keywords': ''
            })
        return layer_list
