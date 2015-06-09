import unittest
from PyQt4.QtCore import QSettings
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.test import utils
from opengeo.gui.gsexploreritems import GsCatalogItem
from opengeo.gui.pgexploreritems import PgConnectionItem
import sys



class ExplorerIntegrationTest(unittest.TestCase):

    __test__ = False


    def _getItemUnder(self, parent, name):
        for idx in range(parent.childCount()):
            item = parent.child(idx)
            if item.text(0) == name:
                return item

    def getStoreItem(self, ws, name):
        return self._getItemUnder(self.getWorkspaceItem(ws), name)

    def getWorkspaceItem(self, name):
        return self._getItemUnder(self.getWorkspacesItem(), name)

    def getLayerItem(self, name):
        return self._getItemUnder(self.getLayersItem(), name)

    def getGroupItem(self, name):
        return self._getItemUnder(self.getGroupsItem(), name)

    def getStyleItem(self, name):
        return self._getItemUnder(self.getStylesItem(), name)

    def getWorkspacesItem(self):
        return self.catalogItem.child(0)

    def getLayersItem(self):
        return self.catalogItem.child(1)

    def getGroupsItem(self):
        return self.catalogItem.child(2)

    def getStylesItem(self):
        return self.catalogItem.child(3)

    def getPGConnectionsItem(self):
        return self.explorer.explorerWidget.pgItem

    def getPGConnectionItem(self):
        return self.pgItem

    def getPGSchemaItem(self, name):
        return self._getItemUnder(self.getPGConnectionItem(), name)

    def getPGTableItem(self, table, schema = "public"):
        return self._getItemUnder(self.getPGSchemaItem(schema), table)

    def getQgsLayersItem(self):
        return self.explorer.explorerWidget.qgsItem.child(0)

    def getQgsLayerItem(self, name):
        return self._getItemUnder(self.getQgsLayersItem(), name)

    def getQgsGroupsItem(self):
        return self.explorer.explorerWidget.qgsItem.child(1)

    def getQgsGroupItem(self, name):
        return self._getItemUnder(self.getQgsGroupsItem(), name)

    def getQgsStylesItem(self):
        return self.explorer.explorerWidget.qgsItem.child(2)

    def getQgsStyleItem(self, name):
        return self._getItemUnder(self.getQgsStylesItem(), "Style of layer '%s'" % name)

    def getGWCLayersItem(self):
        return self.catalogItem.child(4)

    def getGWCLayerItem(self, name):
        return self._getItemUnder(self.getGWCLayersItem(), name)

