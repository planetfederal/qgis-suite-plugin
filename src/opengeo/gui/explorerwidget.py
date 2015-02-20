import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from opengeo.gui.explorertree import ExplorerTreeWidget
from opengeo.gui.gsexploreritems import GsCatalogsItem
from opengeo.gui.pgexploreritems import PgConnectionsItem
from opengeo.gui.qgsexploreritems import QgsProjectItem
from opengeo.gui.treepanels import GsTreePanel, QgsTreePanel, PgTreePanel


class ExplorerWidget(QtGui.QWidget):
    def __init__(self, explorer, singletab = False):
        self.explorer = explorer
        self.singletab = singletab
        QtGui.QWidget.__init__(self, None)
        self.qgsItem = None
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(2)
        verticalLayout.setMargin(0)
        if singletab:
            self.tree = ExplorerTreeWidget(explorer)
            verticalLayout.addWidget(self.tree)
        else:
            self.tabbedPanel = QtGui.QTabWidget()
            self.tabbedPanel.setVisible(True)
            verticalLayout.addWidget(self.tabbedPanel)
        self.setLayout(verticalLayout)
        self.fillData()

    def fillData(self):
        if self.singletab:
            self.gsItem = GsCatalogsItem()
            self.pgItem = PgConnectionsItem()
            self.pgItem.populate()
            self.qgsItem = QgsProjectItem()
            self.qgsItem.populate()
            self.tree.addTopLevelItem(self.gsItem)
            self.tree.addTopLevelItem(self.pgItem)
            self.tree.addTopLevelItem(self.qgsItem)
        else:
            gsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
            pgIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/postgis.png")
            qgsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/qgis.png")
            self.gsPanel = GsTreePanel(self.explorer)
            self.qgsPanel = QgsTreePanel(self.explorer)
            self.pgPanel = PgTreePanel(self.explorer)
            self.tabbedPanel.addTab(self.gsPanel, gsIcon, 'GeoServer')
            self.tabbedPanel.addTab(self.pgPanel, pgIcon,'PostGIS')
            self.tabbedPanel.addTab(self.qgsPanel, qgsIcon, 'QGIS')


    def catalogs(self):
        if self.singletab:
            return self.gsItem._catalogs
        else:
            return self.gsPanel.catalogs

    def pgDatabases(self):
        if self.singletab:
            return self.pgItem.databases
        else:
            return self.pgPanel.databases()

    def currentTreeWidget(self):
        if self.singletab:
            return self.tree
        else:
            return self.tabbedPanel.currentWidget()

    def currentTree(self):
        if self.singletab:
            return self.tree
        else:
            return self.tabbedPanel.currentWidget().tree

    def updateQgisContent(self):
        if self.singletab:
            self.qgsItem.refreshContent(self.explorer)
        else:
            self.qgsPanel.refreshContent()


    def refreshContent(self):
        tree = self.currentTreeWidget()
        if tree is not None:
            tree.refreshContent()