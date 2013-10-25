import unittest
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.geoserver.catalog import Catalog
from opengeo.gui.gsexploreritems import GsCatalogItem
import os
from opengeo.test import utils
from opengeo.test.utils import PT1, WORKSPACE, WORKSPACEB, STYLE, PT2, PT3,\
    GROUP

class DragDropTests(unittest.TestCase):    

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
        #=======================================================================
        # for store in cls.cat.get_stores("test"):
        #    cls.cat.delete(store)
        # ws = cls.cat.get_workspace("test")
        # cls.cat.delete(ws)
        # ws = cls.cat.get_workspace("test")
        # assert ws is None
        # for store in cls.cat.get_stores("testb"):
        #    cls.cat.delete(store)
        # ws = cls.cat.get_workspace("testb")
        # cls.cat.delete(ws)
        # ws = cls.cat.get_workspace("testb")
        # assert ws is None
        # group = cls.cat.get_layergroup("test_group")
        # cls.cat.delete(group)
        # group = cls.cat.get_layergroup("test_group")
        # assert group is None
        # style = cls.cat.get_style("test_points_style")
        # cls.cat.delete(style)
        # style = cls.cat.get_style("test_points_style")
        # assert style is None
        #=======================================================================
        
    def getWorskpaceItem(self, name):
        return self._getItemUnder(self.catalogItem.child(0), name)

    def getLayerItem(self, name):
        return self._getItemUnder(self.catalogItem.child(1), name)
    
    def getGroupItem(self, name):
        return self._getItemUnder(self.catalogItem.child(2), name)
    
    def getStyleItem(self, name):
        return self._getItemUnder(self.catalogItem.child(3), name)
    
    def getWorkspacesItem(self):
        return self.catalogItem.child(0)

    def getLayersItem(self):
        return self.catalogItem.child(1)
    
    def getGroupsItem(self):
        return self.catalogItem.child(2)
    
    def getStylesItem(self):
        return self.catalogItem.child(3)
                    
    def _getItemUnder(self, parent, name):
        for idx in range(parent.childCount()):
            item = parent.child(idx)
            if item.text(0) == name:
                return item
            
    def getQgsLayersItem(self):
        return self.explorer.explorerWidget.qgsItem.child(0)
    
    def getQgsLayerItem(self, name):
        return self._getItemUnder(self.getQgsLayersItem(), name)             

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
        item = self.getWorskpaceItem(WORKSPACEB)        
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
    
    def testDropStyleInLayerItem(self):        
        styleItem = self.getStyleItem(STYLE)
        layerItem = self.getLayerItem(PT2)
        layerItem.acceptDroppedItems(self.tree, self.explorer, [styleItem]) 
        self.assertIsNotNone(self._getItemUnder(layerItem, STYLE)) 
               
    def testDropLayerInGroupItem(self):        
        groupItem = self.getGroupItem(GROUP)
        childCount = groupItem.childCount()
        layerItem = self.getLayerItem(PT3)
        groupItem.acceptDroppedItems(self.tree, self.explorer, [layerItem]) 
        self.assertEquals(childCount + 1, groupItem.childCount())  
        
    def testDropQgisLayerInLayersItem(self):
        layerItem = self.getQgsLayerItem(PT1)        
        layersItem = self.getLayersItem()
        layersItem.acceptDroppedItems(self.tree, self.explorer, [layerItem]) 
        layer = self.cat.get_layer(PT1)
        self.assertIsNotNone(layer)
        self.cat.get_store(PT1, WORKSPACE)
        self.cat.delete(self.cat.get_layer(PT1), recurse = True)
        self.cat.delete(self.cat.get_style(PT1), purge = True)    
                      

def suite():
    suite = unittest.makeSuite(DragDropTests, 'test')
    return suite


def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result