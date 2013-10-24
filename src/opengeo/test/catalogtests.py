import unittest
from opengeo.qgis.catalog import createGeoServerCatalog
import os
from opengeo.qgis import layers
from qgis.core import *
from PyQt4.QtCore import *

class CatalogTests(unittest.TestCase):
    '''
    Tests for the OGCatalog class that provides additional capabilities to a gsconfig catalog
    Requires a Geoserver catalog running on localhost:8080 with default credentials
    and a PostGIS database on localhost:54321 with default credentials (postgres/postgres)    
    '''

    @classmethod
    def setUpClass(cls):
        ''' 'test' workspace cannot exist in the test catalog'''
        cls.cat = createGeoServerCatalog()
        cls.cat.catalog.create_workspace("test", "http://boundlessgeo.com")
        cls.ws = cls.cat.catalog.get_workspace("test")
        assert cls.ws is not None
        
    @classmethod
    def tearDownClass(cls):
        pass
        #TODO remove test catalog
        
        
    def testVectorLayerRoundTrip(self):
        self.cat.publishLayer("pt1", self.ws, name = "pt1gs")
        self.assertIsNotNone(self.cat.catalog.get_layer("pt1gs"))        
        self.cat.addLayerToProject("pt1gs")
        layer = layers.resolveLayer("pt1gs")
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        self.cat.catalog.delete(self.cat.catalog.get_layer("pt1gs"), recurse = True)
        #TODO: more checking to ensure that the layer in the project is correct
                
    def testRasterLayerRoundTrip(self):        
        self.cat.publishLayer("dem", self.ws, name = "demgs")
        self.assertIsNotNone(self.cat.catalog.get_layer("demgs"))        
        
        ''' This will fail due to the GeoServer REST API. If the layer is not under a namespace, it seems is not exposed as WCS'''
        self.cat.addLayerToProject("demgs")
        layer = layers.resolveLayer("demgs")
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        self.cat.catalog.delete(self.cat.catalog.get_layer("demgs"), recurse = True) 
        #TODO: more checking to ensure that the layer in the project is correct              
        
    def testVectorLayerUncompatibleFormat(self):
        self.cat.publishLayer("pt1json", self.ws)
        self.assertIsNotNone(self.cat.catalog.get_layer("pt1json"))
        self.cat.catalog.delete(self.cat.catalog.get_layer("pt1json"), recurse = True)
    
    def testRasterLayerUncompatibleFormat(self):
        self.cat.publishLayer("demascii", self.ws)
        self.assertIsNotNone(self.cat.catalog.get_layer("demascii"))
        self.cat.catalog.delete(self.cat.catalog.get_layer("demascii"), recurse = True)
    
    def testVectorStylingUpload(self):
        self.cat.publishLayer("pt1", self.ws)
        self.assertIsNotNone(self.cat.catalog.get_layer("pt1"))
        sldfile = os.path.join(os.path.dirname(__file__), "resources", "vector.sld")
        with open(sldfile, 'r') as f:
            sld = f.read()
        gssld = self.cat.catalog.get_style("pt1").sld_body
        self.assertEqual(sld, gssld)
        self.cat.catalog.delete(self.cat.catalog.get_layer("pt1"), recurse = True)
        
    def testRasterStylingUpload(self):
        self.cat.publishLayer("dem", self.ws)
        self.assertIsNotNone(self.cat.catalog.get_layer("dem"))
        sldfile = os.path.join(os.path.dirname(__file__), "resources", "raster.sld")
        with open(sldfile, 'r') as f:
            sld = f.read()
        gssld = self.cat.catalog.get_style("dem").sld_body
        self.assertEqual(sld, gssld)
        self.cat.catalog.delete(self.cat.catalog.get_layer("dem"), recurse = True)
        
    def testGroup(self):
        self.cat.publishGroup("geology_landuse", self.ws)
        group = self.cat.catalog.get_group("geology_landuse")
        self.assertIsNotNone(group)
        layers = group.layers
        for layer in layers:
            self.assertIsNotNone(self.cat.catalog.get_layer(layer))
        self.assertTrue("geoforms" in layers)
        self.assertTrue("landuse" in layers)
        self.cat.catalog.delete(self.cat.catalog.get_group("geology_landuse"))
        self.cat.catalog.delete(self.cat.catalog.get_layer("geoforms"), recurse = True)
        self.cat.catalog.delete(self.cat.catalog.get_layer("landuse"), recurse = True)
        
    def testPreuploadVectorHook(self):
        settings = QSettings()
        oldHookFile = str(settings.value("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", ""))
        hookFile = os.path.join(os.path.dirname(__file__), "resources", "vector_hook.py")
        settings.setValue("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", hookFile)        
        self.cat.publishLayer("pt1", self.ws, name = "hook")
        self.assertIsNotNone(self.cat.catalog.get_layer("hook"))
        self.cat.addLayerToProject("hook")
        layer = layers.resolveLayer("hook")
        self.assertEqual(1, layer.featureCount())
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())         
        settings.setValue("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", oldHookFile)
        self.cat.catalog.delete(self.cat.catalog.get_layer("hook"), recurse = True)   


def suite():
    suite = unittest.makeSuite(CatalogTests, 'test')
    return suite


def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result
