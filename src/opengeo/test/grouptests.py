import unittest
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtTest import QTest
from opengeo.gui.explorer import OpenGeoExplorer
from opengeo.gui.dialogs.groupdialog import LayerGroupDialog
from opengeo.test.utils import *
from opengeo.qgis import layers

from opengeo.gui.gsexploreritems import GsCatalogItem
from opengeo.gui.pgexploreritems import PgConnectionItem
import sys

class GroupDialogTests(unittest.TestCase):

    __test__ = True

    @classmethod
    def setUpClass(cls):
        cls.explorer = OpenGeoExplorer(singletab = True)
        cls.cat = getGeoServerCatalog().catalog
        populateCatalog(cls.cat)
        cls.catalogItem = GsCatalogItem(cls.cat, "catalog", "")
        cls.explorer.explorerWidget.gsItem.addChild(cls.catalogItem)
        cls.catalogItem.populate()
        cls.tree = cls.explorer.explorerWidget.tree
        cls.conn = getPostgresConnection()
        cls.pgItem = PgConnectionItem(cls.conn)
        cls.explorer.explorerWidget.pgItem.addChild(cls.pgItem)
        # @TODO - make tests pass using importer
        cls.useRestApi = QSettings().setValue("/OpenGeo/Settings/GeoServer/UseRestApi", True)

    @classmethod
    def tearDownClass(cls):
        cleanCatalog(cls.cat)
        cleanDatabase(cls.conn)


    def testGroupDialogWithEmptyName(self):
        dialog = LayerGroupDialog(self.cat)
        dialog.nameBox.setName("")
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        self.assertFalse(okWidget.isEnabled())

    def testGroupDialogWithNameContaingBlankSpaces(self):
        dialog = LayerGroupDialog(self.cat)
        dialog.nameBox.setName("my group")
        dialog.table.cellWidget(0, 0).setChecked(True)
        okWidget = dialog.buttonBox.button(dialog.buttonBox.Ok)
        self.assertFalse(okWidget.isEnabled())

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