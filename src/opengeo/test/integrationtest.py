import unittest
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.geoserver.catalog import Catalog
from opengeo.test import utils
from opengeo.gui.gsexploreritems import GsCatalogItem



class ExplorerIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.cat = Catalog("http://localhost:8080/geoserver/rest", "admin", "geoserver")
        utils.populateCatalog(cls.cat)
        cls.catalogItem = GsCatalogItem(cls.cat, "catalog", "")
        cls.explorer.explorerWidget.gsItem.addChild(cls.catalogItem)
        cls.catalogItem.populate()
        cls.tree = cls.explorer.explorerWidget.tree

    @classmethod
    def tearDownClass(cls):
        utils.cleanCatalog(cls.cat)
        
    def _getItemUnder(self, parent, name):
        for idx in range(parent.childCount()):
            item = parent.child(idx)
            itemName = item.text(0)
            if item.text(0) == name:
                return item

    def getWorskpaceItem(self, name):
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
        return self._getItemUnder(self.getPGConnectionsItem(), "opengeo")
    
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

  