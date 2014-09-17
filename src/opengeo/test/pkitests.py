import unittest
from qgis.core import *
import sys


class PKITests(unittest.TestCase):
    '''
    Tests for the OGCatalog class that provides additional capabilities to a gsconfig catalog
    Requires a Geoserver catalog with pki auth on localhost:8443 with a catalog named test_catalog
    and a vector layer called test_layer
    '''

    def testOpenWFSLayer(self):
        uri = "http://localhost:8443/geoserver/wfs?srsname=EPSG:4326&typename=\
              polygons&version=1.0.0&request=GetFeature&service=WFS"
        vlayer = QgsVectorLayer(uri, "my_wfs_layer", "WFS")
        self.assertTrue(vlayer.isValid())

    def testOpenWMSLayer(self):
        uri = 'http://localhost:8443/geoserver/wms?layers=polygons&format=image/jpeg&crs=EPSG:4326'
        rlayer = QgsRasterLayer(uri, 'my_wms_layer', 'wms')
        self.assertTrue(rlayer.isValid())

def suite():
    suite = unittest.makeSuite(PKITests, 'test')
    return suite

def run_tests():
    demo_test = unittest.TestLoader().loadTestsFromTestCase(PKITests)
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(demo_test)