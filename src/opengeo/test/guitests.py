import unittest
from opengeo.qgis.catalog import createGeoServerCatalog
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtTest import QTest
from opengeo.gui.dialogs.catalogdialog import DefineCatalogDialog
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.dialogs.groupdialog import LayerGroupDialog
from opengeo.test.integrationtest import ExplorerIntegrationTest
from opengeo.test.utils import GROUP, WORKSPACE, WORKSPACEB, cleanCatalog, PT2,\
    PT1, PUBLIC_SCHEMA
from opengeo.gui.dialogs.layerdialog import PublishLayerDialog,\
    PublishLayersDialog
from opengeo.geoserver.catalog import Catalog
from opengeo.qgis import layers
from opengeo.gui.dialogs.importvector import ImportIntoPostGISDialog
from opengeo.postgis.connection import PgConnection
from opengeo.postgis.schema import Schema

class CreateCatalogDialogTests(unittest.TestCase):
    
    explorer = OpenGeoExplorer(singletab = True)

    def setUp(self):        
        self.cat = createGeoServerCatalog()        
            
    def testCreateCatalogDialog(self):
        dialog = DefineCatalogDialog(self.explorer)
        dialog.nameBox.setText("name")
        dialog.urlBox.setText("http://localhost:8080/geoserver")
        dialog.passwordBox.setText("password")
        dialog.usernameBox.setText("username")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dialog.ok)
        self.assertEquals("username", dialog.username)
        self.assertEquals("password", dialog.password)
        self.assertEquals("name", dialog.name)
        self.assertEquals("http://localhost:8080/geoserver/rest", dialog.url)
        settings = QSettings()
        settings.endGroup(); 
        settings.beginGroup("/OpenGeo/GeoServer/name") 
        settings.remove(""); 
        settings.endGroup(); 
        
    def testCreateCatalogDialogWithUrlWithoutProtocol(self):
        dialog = DefineCatalogDialog(self.explorer)
        dialog.nameBox.setText("name")
        dialog.urlBox.setText("localhost:8080/geoserver")
        dialog.passwordBox.setText("password")
        dialog.usernameBox.setText("username")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dialog.ok)
        self.assertEquals("username", dialog.username)
        self.assertEquals("password", dialog.password)
        self.assertEquals("name", dialog.name)
        self.assertEquals("http://localhost:8080/geoserver/rest", dialog.url)
        settings = QSettings()
        settings.endGroup(); 
        settings.beginGroup("/OpenGeo/GeoServer/name") 
        settings.remove(""); 
        settings.endGroup();             
        
    def testCreateCatalogDialogUsingExistingName(self):
        self.explorer.catalogs()["name"] = self.cat
        dialog = DefineCatalogDialog(self.explorer)
        dialog.nameBox.setText("name")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEquals("name_2", dialog.name)
        settings = QSettings()
        settings.beginGroup("/OpenGeo/GeoServer/name") 
        settings.remove(""); 
        settings.endGroup(); 
        settings.beginGroup("/OpenGeo/GeoServer/name_2") 
        settings.remove(""); 
        settings.endGroup();        
        del self.explorer.catalogs()["name"]
        
    def testLastCatalogNameIsShownByDefault(self):        
        dialog = DefineCatalogDialog(self.explorer)
        dialog.nameBox.setText("catalogname")
        dialog.urlBox.setText("localhost:8081/geoserver")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dialog.ok)
        self.assertEquals("catalogname", dialog.name)
        self.assertEquals("http://localhost:8081/geoserver/rest", dialog.url)
        dialog = DefineCatalogDialog(self.explorer)                
        self.assertEquals("catalogname", dialog.nameBox.text())
        self.assertEquals("localhost:8081/geoserver", dialog.urlBox.text())
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        settings = QSettings()
        settings.endGroup(); 
        settings.beginGroup("/OpenGeo/GeoServer/catalogname") 
        settings.remove(""); 
        settings.endGroup();
     
class GroupDialogTests(ExplorerIntegrationTest):
    
    explorer = OpenGeoExplorer(singletab = True)
                                        
    def testGroupDialogWithEmptyName(self):
        dialog = LayerGroupDialog(self.cat)
        dialog.nameBox.setText("")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertIsNone(dialog.group)
        self.assertEquals("QLineEdit{background: yellow}", dialog.nameBox.styleSheet())
        
    def testGroupDialogWithNameContaingBlankSpaces(self):
        dialog = LayerGroupDialog(self.cat)
        dialog.nameBox.setText("my group")
        dialog.table.cellWidget(0, 0).setChecked(True)
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertIsNotNone(dialog.group)
        self.assertEquals("my_group", dialog.group.name)
    
    def testSelectAllButton(self):
        dialog = LayerGroupDialog(self.cat)        
        QTest.mouseClick(dialog.selectAllButton, Qt.LeftButton)
        for i in range(dialog.table.rowCount()):
            self.assertTrue(dialog.table.cellWidget(i, 0).isChecked())
        QTest.mouseClick(dialog.selectAllButton, Qt.LeftButton)
        for i in range(dialog.table.rowCount()):
            self.assertFalse(dialog.table.cellWidget(i, 0).isChecked())            
                
    def testCannotEditName(self):
        group = self.cat.get_layergroup(GROUP)
        self.assertIsNotNone(group)
        dialog = LayerGroupDialog(self.cat, group)
        self.assertFalse(dialog.nameBox.isEnabled())

class LayerDialogTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.cat = Catalog("http://localhost:8080/geoserver/rest", "admin", "geoserver")
        cls.catalogs = {"catalog": cls.cat} 
        cls.cat.create_workspace(WORKSPACE, "http://test1.com")
        cls.cat.create_workspace(WORKSPACEB, "http://test2.com")     
        
    @classmethod
    def tearDownClass(cls):
        cleanCatalog(cls.cat)
            
    def testPublishLayerDialog(self):        
        dialog = PublishLayerDialog(self.catalogs)        
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertIsNotNone(dialog.catalog)
        self.assertIsNotNone(dialog.workspace)
        dialog = PublishLayerDialog(self.catalogs)        
        cancelWidget = dialog.buttonBox.button(dialog.buttonBox.Cancel)
        QTest.mouseClick(cancelWidget, Qt.LeftButton)
        self.assertIsNone(dialog.catalog)
        self.assertIsNone(dialog.workspace)
         
    def testPublishLayersDialog(self):
        pt1 = layers.resolveLayer(PT1)
        pt2 = layers.resolveLayer(PT2)
        dialog = PublishLayersDialog(self.catalogs, [pt1,pt2])
        cancelWidget = dialog.buttonBox.button(dialog.buttonBox.Cancel)
        QTest.mouseClick(cancelWidget, Qt.LeftButton)
        self.assertIsNone(dialog.topublish)
        
        cat = self.catalogs.values()[0]
        for idx, ws in enumerate(cat.get_workspaces()):
            if ws.name == WORKSPACE:
                wsIdx = idx
            if ws.name == WORKSPACEB:
                wsIdxB = idx                
        dialog = PublishLayersDialog(self.catalogs, [pt1,pt2])
        self.assertEquals(1, dialog.table.columnCount())
        self.assertEquals(2, dialog.table.rowCount())   
        dialog.table.cellWidget(0,0).setCurrentIndex(wsIdx)
        dialog.table.cellWidget(1,0).setCurrentIndex(wsIdxB)            
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertIsNotNone(dialog.topublish)
        self.assertEquals(WORKSPACE, dialog.topublish[0][2].name)
        self.assertEquals(WORKSPACEB, dialog.topublish[1][2].name)
                
        dialog = PublishLayersDialog({"catalog": cat, "catalog2:": cat}, [pt1,pt2])
        self.assertEquals(2, dialog.table.columnCount())
        self.assertEquals(2, dialog.table.rowCount())
        dialog.table.cellWidget(0,1).setCurrentIndex(wsIdx)
        dialog.table.cellWidget(1,1).setCurrentIndex(wsIdxB)
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertIsNotNone(dialog.topublish)
        self.assertEquals(WORKSPACE, dialog.topublish[0][2].name)
        self.assertEquals(WORKSPACEB, dialog.topublish[1][2].name)

class ImportVectorDialogTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.conn1 = PgConnection("conn1", "localhost", 54321,
                            "opengeo", "postgres", "postgres")
        cls.conn2 = PgConnection("conn2", "localhost", 54321,
                            "opengeo", "postgres", "postgres")
        cls.toImport = [layers.resolveLayer(PT1)]             
               
    def testImportVectorDialog(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2], toImport = self.toImport)        
        self.assertEquals(2, dlg.connectionBox.count())
        self.assertTrue(dlg.connectionBox.isEnabled())
        self.assertTrue(dlg.schemaBox.isEnabled())
        okWidget = dlg.buttonBox.button(dlg.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dlg.ok)
        self.assertEquals(1, len(dlg.toImport))
        self.assertIsNone(dlg.tablename)
        
    def testImportVectorDialogWithTablename(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2], toImport = self.toImport)        
        self.assertEquals(2, dlg.connectionBox.count())
        self.assertTrue(dlg.connectionBox.isEnabled())
        self.assertTrue(dlg.schemaBox.isEnabled())
        dlg.tableBox.setEditText("tablename")
        okWidget = dlg.buttonBox.button(dlg.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dlg.ok)
        self.assertEquals(1, len(dlg.toImport))
        self.assertEquals("tablename", dlg.tablename)        
        
    def testImportVectorDialogCancelClicked(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2], toImport = self.toImport)                
        cancelWidget = dlg.buttonBox.button(dlg.buttonBox.Cancel)
        QTest.mouseClick(cancelWidget, Qt.LeftButton)
        self.assertFalse(dlg.ok)
        
    def testImportVectorDialogNothingToImport(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2],)                
        okWidget = dlg.buttonBox.button(dlg.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertFalse(dlg.ok)     
        
    def testImportVectorDialogUsingConnection(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2], connection = self.conn1,
                                       toImport = self.toImport)        
        self.assertEquals(2, dlg.connectionBox.count())
        self.assertFalse(dlg.connectionBox.isEnabled())
        self.assertTrue(dlg.schemaBox.isEnabled())
        okWidget = dlg.buttonBox.button(dlg.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dlg.ok)
        self.assertEquals(1, len(dlg.toImport))
        self.assertIsNone(dlg.tablename)   
        
    def testImportVectorDialogUsingSchema(self):        
        dlg = ImportIntoPostGISDialog([self.conn1, self.conn2], connection = self.conn1, 
                                      schema = Schema(self.conn1, PUBLIC_SCHEMA), toImport = self.toImport)        
        self.assertEquals(2, dlg.connectionBox.count())
        self.assertFalse(dlg.connectionBox.isEnabled())
        self.assertFalse(dlg.schemaBox.isEnabled())
        okWidget = dlg.buttonBox.button(dlg.buttonBox.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertTrue(dlg.ok)
        self.assertEquals(1, len(dlg.toImport))
        self.assertIsNone(dlg.tablename)                 
                
        

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(CreateCatalogDialogTests, 'test'))
    suite.addTests(unittest.makeSuite(GroupDialogTests, 'test'))
    suite.addTests(unittest.makeSuite(LayerDialogTests, 'test'))
    return suite

