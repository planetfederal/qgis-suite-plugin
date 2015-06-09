import unittest
import os
from opengeo.test.utils import PT1, WORKSPACE, WORKSPACEB, STYLE, PT2, PT3,\
    GROUP, GEOLOGY_GROUP, LANDUSE, GEOFORMS, PUBLIC_SCHEMA
from opengeo.test.integrationtest import ExplorerIntegrationTest
from opengeo.gui.pgoperations import importToPostGIS
from opengeo.qgis import layers
import sys
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.test import utils
from opengeo.gui.gsexploreritems import GsCatalogItem
from opengeo.gui.pgexploreritems import PgConnectionItem
from PyQt4.QtCore import QSettings

class DragDropTests(ExplorerIntegrationTest):

    __test__ = True

    @classmethod
    def setUpClass(cls):
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.cat = utils.getGeoServerCatalog().catalog
        utils.populateCatalog(cls.cat)
        cls.catalogItem = GsCatalogItem(cls.cat, "catalog", "")
        cls.explorer.explorerWidget.gsItem.addChild(cls.catalogItem)
        cls.catalogItem.populate()
        cls.tree = cls.explorer.explorerWidget.tree
        cls.conn = utils.getPostgresConnection()
        cls.pgItem = PgConnectionItem(cls.conn)
        cls.explorer.explorerWidget.pgItem.addChild(cls.pgItem)
        # @TODO - make tests pass using importer
        cls.useRestApi = QSettings().setValue("/OpenGeo/Settings/GeoServer/UseRestApi", True)

    @classmethod
    def tearDownClass(cls):
        utils.cleanCatalog(cls.cat)
        utils.cleanDatabase(cls.conn)

    #===========================================================================
    # Drag & drop URIs (i.e. from QGIS browser) to a Explorer tree item
    #===========================================================================

    def testDropVectorLayerUriInCatalogItem(self):
        uri = os.path.join(os.path.dirname(__file__), "data", PT1 + ".shp")
        self.catalogItem.acceptDroppedUris(self.tree, self.explorer, [uri])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropVectorLayerUriInWorkspaceItem(self):
        uri = os.path.join(os.path.dirname(__file__), "data", PT1 + ".shp")
        item = self.getWorkspaceItem(WORKSPACEB)
        self.assertIsNotNone(item)
        item.acceptDroppedUris(self.tree, self.explorer, [uri])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACEB)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropVectorLayerUriInLayersItem(self):
        uri = os.path.join(os.path.dirname(__file__), "data", PT1 + ".shp")
        item = self.catalogItem.child(1)
        item.acceptDroppedUris(self.tree, self.explorer, [uri])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    #===========================================================================
    # Drag & drop explorer tree element(s) into another explorer tree element
    #===========================================================================

    def testDropQgsLayerItemInCatalogItem(self):
        layerItem = self.getQgsLayerItem(PT1)
        self.catalogItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropQgsLayerItemInWorkspacesItem(self):
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)



    def testDropGsLayerInGsGroupItem(self):
        groupItem = self.getGroupItem(GROUP)
        childCount = groupItem.childCount()
        layerItem = self.getLayerItem(PT3)
        groupItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        self.assertEquals(childCount + 1, groupItem.childCount())

    def testDropQgisLayerItemInGsLayersItem(self):
        layerItem = self.getQgsLayerItem(PT1)
        layersItem = self.getLayersItem()
        layersItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropQgisGroupItemInGsGroupsItem(self):
        groupItem = self.getQgsGroupItem(GEOLOGY_GROUP)
        groupsItem = self.getGroupsItem()
        groupsItem.acceptDroppedItems(self.tree, self.explorer, [groupItem])
        layer = self.cat.get_layer(LANDUSE)
        self.assertIsNotNone(layer)
        layer = self.cat.get_layer(GEOFORMS)
        self.assertIsNotNone(layer)
        group = self.cat.get_layergroup(GEOLOGY_GROUP)
        self.assertIsNotNone(group)
        self.cat.delete(self.cat.get_layer(LANDUSE), recurse = True)
        self.cat.delete(self.cat.get_layer(GEOFORMS), recurse = True)
        self.cat.delete(self.cat.get_style(LANDUSE), purge = True)
        self.cat.delete(self.cat.get_style(GEOFORMS), purge = True)

    def testDropQgisGroupInCatalogItem(self):
        groupItem = self.getQgsGroupItem(GEOLOGY_GROUP)
        self.catalogItem.acceptDroppedItems(self.tree, self.explorer, [groupItem])
        layer = self.cat.get_layer(LANDUSE)
        self.assertIsNotNone(layer)
        layer = self.cat.get_layer(GEOFORMS)
        self.assertIsNotNone(layer)
        group = self.cat.get_layergroup(GEOLOGY_GROUP)
        self.assertIsNotNone(group)
        self.cat.delete(self.cat.get_layer(LANDUSE), recurse = True)
        self.cat.delete(self.cat.get_layer(GEOFORMS), recurse = True)
        self.cat.delete(self.cat.get_style(LANDUSE), purge = True)
        self.cat.delete(self.cat.get_style(GEOFORMS), purge = True)

    def testDropQgisGroupInWorkspaceItem(self):
        groupItem = self.getQgsGroupItem(GEOLOGY_GROUP)
        wsItem = self.getWorkspaceItem(WORKSPACEB)
        wsItem.acceptDroppedItems(self.tree, self.explorer, [groupItem])
        layer = self.cat.get_layer(LANDUSE)
        self.assertIsNotNone(layer)
        layer = self.cat.get_layer(GEOFORMS)
        self.assertIsNotNone(layer)
        group = self.cat.get_layergroup(GEOLOGY_GROUP)
        self.assertIsNotNone(group)
        self.cat.get_store(GEOFORMS, WORKSPACEB)
        self.cat.get_store(LANDUSE, WORKSPACEB)
        self.cat.delete(self.cat.get_layer(LANDUSE), recurse = True)
        self.cat.delete(self.cat.get_layer(GEOFORMS), recurse = True)
        self.cat.delete(self.cat.get_style(LANDUSE), purge = True)
        self.cat.delete(self.cat.get_style(GEOFORMS), purge = True)

    def testDropQgisStyleInStylesItem(self):
        styleItem = self.getQgsStyleItem(PT1)
        stylesItem = self.getStylesItem()
        stylesItem.acceptDroppedItems(self.tree, self.explorer, [styleItem])
        style = self.cat.get_style(PT1)
        self.assertIsNotNone(style)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropQgisLayerItemInWorkspaceItem(self):
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspaceItem(WORKSPACEB)
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACEB)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)

    def testDropPGTableInGsLayersItem(self):
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1)], PUBLIC_SCHEMA, PT1, False, False);
        self.getPGConnectionItem().refreshContent(self.explorer)
        tableItem = self.getPGTableItem(PT1)
        self.assertIsNotNone(tableItem)
        layersItem = self.getLayersItem()
        layersItem.acceptDroppedItems(self.tree, self.explorer, [tableItem])
        tableLayerName = PT1 + "_table"
        layer = self.cat.get_layer(tableLayerName)
        self.assertIsNotNone(layer)
        self.cat.delete(self.cat.get_layer(tableLayerName), recurse = True)

    def testDropPGTableInWorkspacesItem(self):
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1)], PUBLIC_SCHEMA, PT1, False, False);
        self.getPGConnectionItem().refreshContent(self.explorer)
        tableItem = self.getPGTableItem(PT1)
        self.assertIsNotNone(tableItem)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [tableItem])
        tableLayerName = PT1 + "_table"
        layer = self.cat.get_layer(tableLayerName)
        self.assertIsNotNone(layer)
        self.cat.delete(self.cat.get_layer(tableLayerName), recurse = True)



    def testDropGsStyleInGsLayerItem(self):
        styleItem = self.getStyleItem(STYLE)
        self.assertIsNotNone(styleItem)
        layerItem = self.getLayerItem(PT2)
        self.assertIsNotNone(layerItem)
        self.assertEquals(1, layerItem.childCount())
        self.assertEquals(len(self.cat.get_layer(PT2).styles), 0)
        layerItem.acceptDroppedItems(self.tree, self.explorer, [styleItem])
        self.assertEquals(len(self.cat.get_layer(PT2).styles), 1)


def suite():
    suite = unittest.makeSuite(DragDropTests, 'test')
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())