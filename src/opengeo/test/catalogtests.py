import unittest
from opengeo.qgis.catalog import createGeoServerCatalog
import os
from opengeo.qgis import layers
from qgis.core import *
from PyQt4.QtCore import *
from opengeo.test import utils
from opengeo.test.utils import PT1, DEM, PT1JSON, DEMASCII,\
    GEOLOGY_GROUP, GEOFORMS, LANDUSE, HOOK, WORKSPACE

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
        utils.cleanCatalog(cls.cat.catalog)
        cls.cat.catalog.create_workspace(WORKSPACE, "http://boundlessgeo.com")
        cls.ws = cls.cat.catalog.get_workspace(WORKSPACE)
        assert cls.ws is not None
        
    @classmethod
    def tearDownClass(cls):
        utils.cleanCatalog(cls.cat.catalog)        
        
        
    def testVectorLayerRoundTrip(self):
        self.cat.publishLayer(PT1, self.ws, name = PT1)
        self.assertIsNotNone(self.cat.catalog.get_layer(PT1))        
        self.cat.addLayerToProject(PT1, "pt1")
        layer = layers.resolveLayer("pt1")
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        self.cat.catalog.delete(self.cat.catalog.get_layer(PT1), recurse = True)
        #TODO: more checking to ensure that the layer in the project is correct
                
    def testRasterLayerRoundTrip(self):        
        self.cat.publishLayer(DEM, self.ws, name = DEM)
        self.assertIsNotNone(self.cat.catalog.get_layer(DEM))        
        self.cat.addLayerToProject(DEM, "DEM")
        layer = layers.resolveLayer("DEM")
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        self.cat.catalog.delete(self.cat.catalog.get_layer(DEM), recurse = True) 
        #TODO: more checking to ensure that the layer in the project is correct              
        
    def testVectorLayerUncompatibleFormat(self):
        self.cat.publishLayer(PT1JSON, self.ws, name = PT1JSON)
        self.assertIsNotNone(self.cat.catalog.get_layer(PT1JSON))
        self.cat.catalog.delete(self.cat.catalog.get_layer(PT1JSON), recurse = True)
    
    def testRasterLayerUncompatibleFormat(self):
        self.cat.publishLayer(DEMASCII, self.ws, name = DEMASCII)
        self.assertIsNotNone(self.cat.catalog.get_layer(DEMASCII))
        self.cat.catalog.delete(self.cat.catalog.get_layer(DEMASCII), recurse = True)
    
    def testVectorStylingUpload(self):
        self.cat.publishLayer(PT1, self.ws, name = PT1)
        self.assertIsNotNone(self.cat.catalog.get_layer(PT1))
        sldfile = os.path.join(os.path.dirname(__file__), "resources", "vector.sld")
        with open(sldfile, 'r') as f:
            sld = f.read()
        gssld = self.cat.catalog.get_style(PT1).sld_body
        self.assertEqual(sld, gssld)
        self.cat.catalog.delete(self.cat.catalog.get_layer(PT1), recurse = True)
        
    def testRasterStylingUpload(self):
        self.cat.publishLayer(DEM, self.ws, name = DEM)
        self.assertIsNotNone(self.cat.catalog.get_layer(DEM))
        sldfile = os.path.join(os.path.dirname(__file__), "resources", "raster.sld")
        with open(sldfile, 'r') as f:
            sld = f.read()
        gssld = self.cat.catalog.get_style(DEM).sld_body
        self.assertEqual(sld, gssld)
        self.cat.catalog.delete(self.cat.catalog.get_layer(DEM), recurse = True)
        
    def testGroup(self):
        self.cat.publishGroup(GEOLOGY_GROUP, workspace = self.ws)
        group = self.cat.catalog.get_layergroup(GEOLOGY_GROUP)
        self.assertIsNotNone(group)
        layers = group.layers
        for layer in layers:
            self.assertIsNotNone(self.cat.catalog.get_layer(layer))
        self.assertTrue(GEOFORMS in layers)
        self.assertTrue(LANDUSE in layers)
        self.cat.catalog.delete(self.cat.catalog.get_layergroup(GEOLOGY_GROUP))
        self.cat.catalog.delete(self.cat.catalog.get_layer(GEOFORMS), recurse = True)
        self.cat.catalog.delete(self.cat.catalog.get_layer(LANDUSE), recurse = True)
        
    def testPreuploadVectorHook(self):
        settings = QSettings()
        oldHookFile = str(settings.value("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", ""))
        hookFile = os.path.join(os.path.dirname(__file__), "resources", "vector_hook.py")
        settings.setValue("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", hookFile)        
        self.cat.publishLayer(PT1, self.ws, name = HOOK)
        self.assertIsNotNone(self.cat.catalog.get_layer(HOOK))
        self.cat.addLayerToProject(HOOK)
        layer = layers.resolveLayer(HOOK)
        self.assertEqual(1, layer.featureCount())
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())         
        settings.setValue("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", oldHookFile)
        self.cat.catalog.delete(self.cat.catalog.get_layer(HOOK), recurse = True)   


def suite():
    suite = unittest.makeSuite(CatalogTests, 'test')
    return suite


def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result
