import unittest
from opengeo.qgis.catalog import createGeoServerCatalog
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtTest import QTest
from opengeo.gui.dialogs.catalogdialog import DefineCatalogDialog
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.dialogs.groupdialog import LayerGroupDialog
from opengeo.test.integrationtest import ExplorerIntegrationTest
from opengeo.test.utils import GROUP

WORKSPACE_NAME = "test"

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


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(CreateCatalogDialogTests, 'test'))
    suite.addTests(unittest.makeSuite(GroupDialogTests, 'test'))
    return suite


def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result
