from opengeo.test.utils import PT1
from opengeo.test.integrationtest import ExplorerIntegrationTest
import unittest
from PyQt4.QtCore import *
from opengeo.qgis.catalog import createGeoServerCatalog


class DeleteTests(ExplorerIntegrationTest):

    
    def testDeleteLayerAndStyle(self):
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)    
        self.getLayersItem().refreshContent(self.explorer)
        self.getStylesItem().refreshContent(self.explorer)      
        settings = QSettings()
        deleteStyle = bool(settings.value("/OpenGeo/Settings/GeoServer/DeleteStyle"))
        settings.setValue("/OpenGeo/Settings/GeoServer/DeleteStyle", True)
        layerItem = self.getLayerItem(PT1)
        layerItem.deleteLayer(self.tree, self.explorer)
        layerItem = self.getLayerItem(PT1)
        self.assertIsNone(layerItem)
        styleItem = self.getStyleItem(PT1)
        self.assertIsNone(styleItem)
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)        
        self.getLayersItem().refreshContent(self.explorer)
        self.getStylesItem().refreshContent(self.explorer)         
        settings.setValue("/OpenGeo/Settings/GeoServer/DeleteStyle", False)
        layerItem = self.getLayerItem(PT1)
        layerItem.deleteLayer(self.tree, self.explorer)
        layerItem = self.getLayerItem(PT1)
        self.assertIsNone(layerItem)
        styleItem = self.getStyleItem(PT1)
        self.assertIsNotNone(styleItem)
        styleItem.deleteStyle(self.tree, self.explorer)
        styleItem = self.getStyleItem(PT1)
        self.assertIsNone(styleItem)
        settings.setValue("/OpenGeo/Settings/GeoServer/DeleteStyle", deleteStyle)


def suite():
    suite = unittest.makeSuite(DeleteTests, 'test')
    return suite
