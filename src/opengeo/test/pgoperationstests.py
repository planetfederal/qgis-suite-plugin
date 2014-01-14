import unittest
from opengeo.qgis import layers
from qgis.core import *
from PyQt4.QtCore import *
from opengeo.test import utils
from opengeo.test.utils import PT1, PUBLIC_SCHEMA, PT2, getPostgresConnection
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.pgoperations import importToPostGIS
from opengeo.postgis.schema import Schema

class PgOperationsTests(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        cls.conn = getPostgresConnection()
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.tree = cls.explorer.explorerWidget.tree
    
    def tearDown(self):
        utils.cleanDatabase(self.conn)        
        
        
    def getTable(self, schema, name):
        tables = schema.tables()        
        for table in tables:
            if table.name == name:
                return table
                
    
    def testImportSingleLayer(self):
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1)], PUBLIC_SCHEMA, PT1, False, False);        
        schema = Schema(self.conn, PUBLIC_SCHEMA)        
        self.assertIsNotNone(self.getTable(schema, PT1))
        
    def testImportSingleLayerAsSingleGeometries(self):
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1)], PUBLIC_SCHEMA, PT1, False, True);        
        schema = Schema(self.conn, PUBLIC_SCHEMA)        
        table = self.getTable(schema, PT1)
        self.assertIsNotNone(table)
        self.assertEquals(-1, table.geomtype.find("MULTI"))        
        
    def testImportMultipleLayers(self):
        importToPostGIS(self.explorer, self.conn, [layers.resolveLayer(PT1), layers.resolveLayer(PT2)], PUBLIC_SCHEMA, None, False, False);        
        schema = Schema(self.conn, PUBLIC_SCHEMA)
        self.assertIsNotNone(self.getTable(schema, PT1))
        self.assertIsNotNone(self.getTable(schema, PT2))
        

def suite():
    suite = unittest.makeSuite(PgOperationsTests, 'test')
    return suite
