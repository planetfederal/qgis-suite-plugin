import unittest
from opengeo.qgis.catalog import createGeoServerCatalog
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtTest import QTest
from opengeo.gui.dialogs.catalogdialog import DefineCatalogDialog
from opengeo.gui.explorer import OpenGeoExplorer

WORKSPACE_NAME = "test"

class CreateCatalogTests(unittest.TestCase):
    
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

def suite():
    suite = unittest.makeSuite(CreateCatalogTests, 'test')
    return suite


def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result
