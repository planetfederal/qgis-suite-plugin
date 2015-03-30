import os
import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from opengeo.gui.exploreritems import TreeItem
from opengeo.qgis import layers as qgislayers
from dialogs.styledialog import PublishStyleDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogselector import selectCatalog
from dialogs.layerdialog import PublishLayersDialog, PublishLayerDialog
from dialogs.groupdialog import PublishLayerGroupDialog
from dialogs.projectdialog import PublishProjectDialog
from opengeo.gui.dialogs.importvector import ImportIntoPostGISDialog
from opengeo import config
from geoserver.catalog import ConflictingDataError
from geoserver.layergroup import UnsavedLayerGroup
from opengeo.gui.dialogs.metatoolseditor import MetatoolsEditor
from opengeo.metadata.metadata_provider import MetadataProvider
from qgis.core import *


class QgsTreeItem(TreeItem):

    def iconPath(self):
        return os.path.dirname(__file__) + "/../images/qgis.png"


def publishProject(tree, explorer):
    layers = qgislayers.getAllLayers()
    if not layers:
        return

    dlg = PublishProjectDialog(explorer.catalogs())
    dlg.exec_()
    catalog = dlg.catalog
    if catalog is None:
        return
    workspace = dlg.workspace
    groupName = dlg.groupName
    ogcat = OGCatalog(catalog)

    groups = qgislayers.getGroups()
    grouplyrs = []
    for group in groups:
        grouplyrs.extend([layer for layer in groups[group]])

    ungroupedlyrs = [layer for layer in layers if layer not in grouplyrs]
    publishedLyrs = []

    if ungroupedlyrs:
        lyrsdlg = PublishLayersDialog(
            {0: catalog}, ungroupedlyrs, workspace=workspace, overwrite=False)
        lyrsdlg.exec_()
        toPublish = lyrsdlg.topublish
        if toPublish is None:
            return

        explorer.setProgressMaximum(len(toPublish), "Publish ungrouped layer")
        progress = 0
        for layer, catalog, workspace, layername in toPublish:
            publishedLyrs.append(layername)
            explorer.setProgress(progress)
            if not explorer.run(ogcat.publishLayer,
                                None,
                                [],
                                layer, workspace, True, layername):
                explorer.setProgress(0)
                return
            progress += 1
            explorer.setProgress(progress)
        explorer.resetActivity()

    for group in groups:
        grouplyrs = [layer for layer in groups[group]]
        if not grouplyrs:
            continue  # don't publish empty groups, when publishing project

        dlg = PublishLayerGroupDialog(catalog, group, grouplyrs,
                                      workspace=workspace,
                                      overwritegroup=False,
                                      overwritelayers=False)
        dlg.exec_()
        grpName = dlg.definedname
        toPublish = dlg.topublish
        if grpName is None:  # toPublish can be empty list
            return

        explorer.setProgressMaximum(len(toPublish), "Publish grouped layer")
        progress = 0
        layernames = []
        for layer, catalog, workspace, layername in toPublish:
            layernames.append(layername)
            publishedLyrs.append(layername)
            explorer.setProgress(progress)
            if not explorer.run(ogcat.publishLayer,
                                None,
                                [],
                                layer, workspace, True, layername):
                explorer.setProgress(0)
                return
            progress += 1
            explorer.setProgress(progress)
        explorer.resetActivity()
        names = reversed(layernames)

        layergroup = catalog.create_layergroup(grpName, names, names)
        if not explorer.run(catalog.save,
                            "Create layer group from group '" + group + "'",
                            [],
                            layergroup):
            return

    if groupName is not None:
        names = reversed(publishedLyrs)
        layergroup = catalog.create_layergroup(groupName, names, names)
        if not explorer.run(catalog.save,
                            "Create global layer group",
                            [],
                            layergroup):
            return

    tree.findAllItems(catalog)[0].refreshContent(explorer)
    explorer.setInfo("Project published")


class QgsProjectItem(QgsTreeItem):
    def __init__(self):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/qgis.png")
        TreeItem.__init__(self, None, icon, "QGIS Project")

    def populate(self):
        layersItem = QgsLayersItem()
        layersItem.populate()
        self.addChild(layersItem)
        groupsItem = QgsGroupsItem()
        groupsItem.populate()
        self.addChild(groupsItem)
        stylesItem = QgsStylesItem()
        stylesItem.populate()
        self.addChild(stylesItem)

    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishProjectAction = QtGui.QAction(icon, "Publish...", explorer)
        publishProjectAction.triggered.connect(lambda: publishProject(tree, explorer))
        publishProjectAction.setEnabled(len(explorer.catalogs())>0)
        return [publishProjectAction]


class QgsLayersItem(QgsTreeItem):
    def __init__(self):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, None, icon, "QGIS Layers")

    def populate(self):
        layers = qgislayers.getAllLayers()
        for layer in layers:
            layerItem = QgsLayerItem(layer)
            self.addChild(layerItem)

    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishProjectAction = QtGui.QAction(icon, "Publish...", explorer)
        publishProjectAction.triggered.connect(lambda: publishProject(tree, explorer))
        publishProjectAction.setEnabled(len(explorer.catalogs())>0)
        return [publishProjectAction]

class QgsGroupsItem(QgsTreeItem):
    def __init__(self):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, None, icon, "QGIS Groups")

    def populate(self):
        groups = qgislayers.getGroups()
        for group in groups:
            groupItem = QgsGroupItem(group)
            self.addChild(groupItem)
            groupItem.populate()

class QgsStylesItem(QgsTreeItem):
    def __init__(self):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeItem.__init__(self, None, icon, "QGIS Styles")

    def populate(self):
        styles = qgislayers.getAllLayers()
        for style in styles:
            styleItem = QgsStyleItem(style)
            self.addChild(styleItem)

class QgsLayerItem(QgsTreeItem):
    def __init__(self, layer ):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, layer, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        if layer is not None and hasattr(layer, 'name') \
                and hasattr(layer, 'publicSource'):
            self.setToolTip(0, "{0}:\n{1}".format(layer.name(),
                layer.publicSource()))

    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishLayerAction = QtGui.QAction(icon, "Publish to GeoServer...", explorer)
        publishLayerAction.triggered.connect(lambda: self.publishLayer(tree, explorer))
        publishLayerAction.setEnabled(len(explorer.catalogs())>0)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/create-store-from-layer.png")
        createStoreFromLayerAction= QtGui.QAction(icon, "Create store from layer...", explorer)
        createStoreFromLayerAction.triggered.connect(lambda: self.createStoreFromLayer(tree, explorer))
        createStoreFromLayerAction.setEnabled(len(explorer.catalogs())>0)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/metadata.png")
        editMetadataAction = QtGui.QAction(icon, "Edit/view layer metadata...", explorer)
        editMetadataAction.triggered.connect(lambda: self.editMetadata(tree, explorer))
        editMetadataAction.setEnabled(True)
        actions =  [publishLayerAction, createStoreFromLayerAction, editMetadataAction]
        if isinstance(self.element, QgsVectorLayer):
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/postgis_import.png")
            importToPostGisAction = QtGui.QAction(icon, "Import into PostGIS...", explorer)
            importToPostGisAction.triggered.connect(lambda: self.importLayerToPostGis(tree, explorer))
            importToPostGisAction.setEnabled(len(explorer.pgDatabases())>0)
            actions.append(importToPostGisAction)

        return actions

    def editMetadata(self, tree, explorer):
        try:
            md = MetadataProvider.getProvider(self.element)
        except Exception, e:
            explorer.setWarning(unicode(e.args[0]))
            return

        self.dlg = MetatoolsEditor(config.iface.mainWindow())
        try:
            self.dlg.setContent(md, self.element)
            self.dlg.show()
        except Exception, e:
            explorer.setWarning("Cannot open layer metadata: " + unicode(e.args[0]))



    def importMetadataFromFile(self, layers, explorer):
        fileName = QtGui.QFileDialog.getOpenFileName(config.iface.mainWindow(),
                                           "Select metadata file",
                                           "",
                                           'XML files (*.xml);;Text files (*.txt *.TXT);;All files (*.*)'
                                          )
        if fileName:
            try:
                for layer in layers:
                    md = MetadataProvider.getProvider(layer)
                    md.importFromFile(unicode(fileName))
                explorer.setInfo("Metadata was imported successfully")
            except Exception, e:
                explorer.setWarning("Metadata can't be imported: " +  e.args[0])


    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishLayersAction = QtGui.QAction(icon, "Publish to GeoServer...", explorer)
        publishLayersAction.triggered.connect(lambda: self.publishLayers(tree, explorer, selected))
        publishLayersAction.setEnabled(len(explorer.catalogs())>0)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/create-store-from-layer.png")
        createStoresFromLayersAction= QtGui.QAction(icon, "Create stores from layers...", explorer)
        createStoresFromLayersAction.triggered.connect(lambda: self.createStoresFromLayers(tree, explorer, selected))
        createStoresFromLayersAction.setEnabled(len(explorer.catalogs())>0)

        importToPostGisAction = QtGui.QAction("Import into PostGIS...", explorer)
        importToPostGisAction.triggered.connect(lambda: self.importLayersToPostGis(tree, explorer, selected))
        importToPostGisAction.setEnabled(len(explorer.pgDatabases())>0)
        importMetadataAction = QtGui.QAction("Import metadata from file...", explorer)
        importMetadataAction.triggered.connect(lambda: self.importMetadataFromFile([item.element for item in selected], explorer))
        importMetadataAction.setEnabled(True)
        return [publishLayersAction, createStoresFromLayersAction, importToPostGisAction, importMetadataAction]

    def publishLayers(self, tree, explorer, selected):
        layers = [item.element for item in selected]
        dlg = PublishLayersDialog(explorer.catalogs(), layers)
        dlg.exec_()
        toPublish = dlg.topublish
        if toPublish is None:
            return
        explorer.setProgressMaximum(len(toPublish), "Publish layers")
        progress = 0
        toUpdate = set()
        for layer, catalog, workspace, layername in toPublish:
            explorer.setProgress(progress)
            ogcat = OGCatalog(catalog)
            if explorer.run(ogcat.publishLayer,
                     None,
                     [],
                     layer, workspace, True, layername):
                toUpdate.add(tree.findAllItems(catalog)[0])
            progress += 1
            explorer.setProgress(progress)

        for item in toUpdate:
            item.refreshContent(explorer)
        explorer.resetActivity()


    def importLayerToPostGis(self, tree, explorer):
        self.importLayersToPostGis(tree, explorer, [self])


    def importLayersToPostGis(self, tree, explorer, selected):
        layers = [item.element for item in selected]
        dlg = ImportIntoPostGISDialog(explorer.pgDatabases(), toImport = layers)
        dlg.exec_()
        if dlg.ok:
            schema = [s for s in dlg.connection.schemas() if s.name == dlg.schema][0]
            if len(dlg.toImport) > 1:
                explorer.setProgressMaximum(len(dlg.toImport), "Import layers to PostGIS")
            for i, layer in enumerate(dlg.toImport):
                explorer.run(dlg.connection.importFileOrLayer,
                            "Import layer into PostGIS",
                            tree.findAllItems(schema),
                            layer, dlg.schema, dlg.tablename, not dlg.add, dlg.single)
                explorer.setProgress(i + 1)
            explorer.resetActivity()



    def createStoresFromLayers(self, tree, explorer, selected):
        layers = [item.element for item in selected]
        dlg = PublishLayersDialog(explorer.catalogs(), layers)
        dlg.exec_()
        toPublish  = dlg.topublish
        if toPublish is None:
            return
        explorer.setProgressMaximum(len(toPublish), "Upload layers")
        progress = 0
        toUpdate = set()
        for layer, catalog, workspace, layername in toPublish:
            explorer.setProgress(progress)
            ogcat = OGCatalog(catalog)
            if explorer.run(ogcat.upload,
                     None,
                     [],
                     layer, workspace, True, layername):
                toUpdate.add(tree.findAllItems(catalog)[0])
            progress += 1
            explorer.setProgress(progress)

        for item in toUpdate:
            item.refreshContent(explorer)
        explorer.resetActivity()

    def createStoreFromLayer(self, tree, explorer):
        dlg = PublishLayerDialog(explorer.catalogs(), self.element)
        dlg.exec_()
        if dlg.catalog is None:
            return
        cat = dlg.catalog
        ogcat = OGCatalog(cat)
        catItem = tree.findAllItems(cat)[0]
        explorer.run(ogcat.upload,
                 "Create store from layer '" + self.element.name() + "'",
                 [catItem],
                 self.element, dlg.workspace, True, dlg.layername)

    def publishLayer(self, tree, explorer):
        dlg = PublishLayerDialog(explorer.catalogs(), self.element)
        dlg.exec_()
        if dlg.catalog is None:
            return
        cat = dlg.catalog
        ogcat = OGCatalog(cat)
        catItem = tree.findAllItems(cat)[0]
        explorer.run(ogcat.publishLayer,
                 "Publish layer '" + self.element.name() + "'",
                 [catItem],
                 self.element, dlg.workspace, True, dlg.layername)


class QgsGroupItem(QgsTreeItem):
    def __init__(self, group):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, group , icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)

    def refreshContent(self, explorer):
        self.parent().refreshContent(explorer)

    def populate(self):
        grouplayers = qgislayers.getGroups()[self.element]
        for layer in grouplayers:
            layerItem = QgsLayerItem(layer)
            self.addChild(layerItem)

    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishGroupAction = QtGui.QAction(icon, "Publish...", explorer)
        publishGroupAction.triggered.connect(lambda: self.publishGroup(tree, explorer))
        publishGroupAction.setEnabled(len(explorer.catalogs())>0)
        return[publishGroupAction]

    def publishGroup(self, tree, explorer):
        groupname = self.element
        groups = qgislayers.getGroups()
        grouplyrs = groups[groupname]

        cat = selectCatalog(explorer.catalogs())
        if cat is None:
            return
        catgroup = cat.get_layergroup(groupname)
        toUpdate = set()
        toUpdate.add(tree.findAllItems(cat)[0])

        overwrite = bool(QSettings().value(
            "/OpenGeo/Settings/GeoServer/OverwriteGroupLayers", True, bool))

        dlg = PublishLayerGroupDialog(cat, groupname, grouplyrs,
                                      overwritegroup=True,
                                      overwritelayers=overwrite)
        dlg.exec_()
        grpName = dlg.definedname
        toPublish = dlg.topublish
        if grpName is None:  # toPublish can be empty list
            return
        catgroup = cat.get_layergroup(grpName)

        names = []
        if toPublish:
            explorer.setProgressMaximum(len(toPublish), "Publish layers")
            progress = 0
            layernames = []
            for layer, catalog, workspace, layername in toPublish:
                layernames.append(layername)
                explorer.setProgress(progress)
                ogcat = OGCatalog(catalog)
                if not explorer.run(ogcat.publishLayer,
                                    None,
                                    [],
                                    layer, workspace, True, layername):
                    explorer.setProgress(0)
                    return
                progress += 1
                explorer.setProgress(progress)
            explorer.resetActivity()
            names = reversed(layernames)

        if catgroup:
            cat.delete(catgroup)

        #TODO calculate bounds
        bbox = None
        group = UnsavedLayerGroup(cat, grpName, names, names, bbox)

        explorer.run(cat.save,
                     "Create layer group from group '" + groupname + "'",
                     toUpdate,
                     group)


class QgsStyleItem(QgsTreeItem):
    def __init__(self, layer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        label = "Style of layer '" + layer.name() + "'"
        TreeItem.__init__(self, layer, icon, label)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        self.setToolTip(0, label)

    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishStyleAction = QtGui.QAction(icon, "Publish...", explorer)
        publishStyleAction.triggered.connect(lambda: self.publishStyle(tree, explorer))
        publishStyleAction.setEnabled(len(explorer.catalogs()) > 0)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit.png")
        editAction = QtGui.QAction(icon, "Edit...", explorer)
        editAction.triggered.connect(lambda: config.iface.showLayerProperties(self.element))
        return [publishStyleAction, editAction]

    def publishStyle(self, tree, explorer):
        dlg = PublishStyleDialog(explorer.catalogs(), self.element.name())
        dlg.exec_()
        if dlg.catalog is None:
            return
        cat = explorer.catalogs()[dlg.catalog]
        ogcat = OGCatalog(cat)
        catItem = tree.findAllItems(cat)[0]
        toUpdate = [catItem.stylesItem]
        explorer.run(ogcat.publishStyle,
                 "Publish style from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, True, dlg.name)
