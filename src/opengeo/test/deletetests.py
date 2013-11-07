from opengeo.test.utils import PT1, safeName
from opengeo.test.integrationtest import ExplorerIntegrationTest
import unittest
from PyQt4.QtCore import *


class DeleteTests(ExplorerIntegrationTest):
    
    def testDeleteLayerAndStyle(self):
        settings = QSettings()
        confirmDelete = settings.value("/OpenGeo/Settings/General/ConfirmDelete", True, bool) 
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)    
        self.getLayersItem().refreshContent(self.explorer)
        self.getStylesItem().refreshContent(self.explorer)              
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
        settings.setValue("/OpenGeo/Settings/General/ConfirmDelete", confirmDelete)
        
    def testDeleteWorkspace(self):
        settings = QSettings()
        confirmDelete = settings.value("/OpenGeo/Settings/General/ConfirmDelete", True, bool) 
        wsname = safeName("another_workspace")
        self.cat.create_workspace(wsname, "http://anothertesturl.com")
        self.getWorkspacesItem().refreshContent(self.explorer)
        wsItem = self.getWorskpaceItem(wsname)
        wsItem.deleteWorkspace(self.tree, self.explorer)
        self.getWorkspacesItem().refreshContent(self.explorer)
        wsItem = self.getWorskpaceItem(wsname)
        self.assertIsNone(wsItem)
        ws = self.cat.get_workspace(wsname)
        self.assertIsNone(ws)
        settings.setValue("/OpenGeo/Settings/General/ConfirmDelete", confirmDelete)
        
        


def suite():
    suite = unittest.makeSuite(DeleteTests, 'test')
    return suite
