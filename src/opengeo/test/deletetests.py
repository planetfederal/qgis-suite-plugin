from opengeo.test.utils import PT1, safeName, OPENGEO_SCHEMA, PUBLIC_SCHEMA, PT2,\
    WORKSPACE
from opengeo.test.integrationtest import ExplorerIntegrationTest
import unittest
from PyQt4.QtCore import *
from opengeo.gui.pgoperations import importToPostGIS
from opengeo.qgis import layers


class DeleteTests(ExplorerIntegrationTest):
    
    @classmethod
    def setUpClass(cls):        
        super(DeleteTests, cls).setUpClass()
        cls.confirmDelete = QSettings().value("/OpenGeo/Settings/General/ConfirmDelete", True, bool)

    @classmethod
    def tearDownClass(cls):
        super(DeleteTests, cls).tearDownClass()        
        QSettings().setValue("/OpenGeo/Settings/General/ConfirmDelete", cls.confirmDelete)
        
    def testDeleteLayerAndStyle(self):
        settings = QSettings()         
        layerItem = self.getQgsLayerItem(PT1)
        wsItem = self.getWorkspacesItem()
        wsItem.acceptDroppedItems(self.tree, self.explorer, [layerItem])
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)    
        self.getLayersItem().refreshContent(self.explorer)
        self.getStylesItem().refreshContent(self.explorer)              
        deleteStyle = bool(settings.value("/OpenGeo/Settings/GeoServer/DeleteStyle"))        
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
        
        
    def testDeleteWorkspace(self):            
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
    
    def testDeleteSchema(self):                
        self.conn.geodb.create_schema(OPENGEO_SCHEMA)
        self.getPGConnectionItem().refreshContent(self.explorer)
        schemaItem = self.getPGSchemaItem(OPENGEO_SCHEMA)
        schemaItem.deleteSchema(self.explorer)
        schemaItem = self.getPGSchemaItem(OPENGEO_SCHEMA)        
        self.assertIsNone(schemaItem)
        
    def testDeleteTable(self):                
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1)], PUBLIC_SCHEMA, PT1, False, False); 
        self.getPGConnectionItem().refreshContent(self.explorer)       
        tableItem = self.getPGTableItem(PT1)
        tableItem.deleteTable(self.explorer)
        tableItem = self.getPGTableItem(PT1)                    
        self.assertIsNone(tableItem)        
               
               
    def testDeleteGWCLayer(self):
        name = WORKSPACE + ":" + PT2
        item = self.getGWCLayerItem(name)
        item.deleteLayer(self.explorer)
        item = self.getGWCLayerItem(name)
        self.assertIsNone(item)


def suite():
    suite = unittest.makeSuite(DeleteTests, 'test')
    return suite
