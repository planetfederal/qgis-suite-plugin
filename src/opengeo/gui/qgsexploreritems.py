import os
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from opengeo.gui.exploreritems import TreeItem
from opengeo.qgis import layers as qgislayers
from dialogs.styledialog import PublishStyleDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogselector import selectCatalog
from dialogs.layerdialog import PublishLayersDialog, PublishLayerDialog
from dialogs.projectdialog import PublishProjectDialog
from opengeo.gui.dialogs.importvector import ImportIntoPostGISDialog
from opengeo import config
from opengeo.gui.overwrite import publishLayer
from opengeo.geoserver.catalog import ConflictingDataError
                
class QgsTreeItem(TreeItem):
    
    def iconPath(self):
        return os.path.dirname(__file__) + "/../images/qgis.png"
        
class QgsProjectItem(QgsTreeItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/qgis.png")
        TreeItem.__init__(self, None, icon, "QGIS project")        
                 
    def populate(self):                    
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        layersItem = QgsTreeItem(None, icon, "QGIS Layers")        
        layersItem.setIcon(0, icon)
        layers = qgislayers.getAllLayers()
        for layer in layers:
            layerItem = QgsLayerItem(layer)            
            layersItem.addChild(layerItem)
        self.addChild(layersItem)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        groupsItem = QgsTreeItem(None, icon, "QGIS Groups")        
        groups = qgislayers.getGroups()
        for group in groups:
            groupItem = QgsGroupItem(group)                                
            groupsItem.addChild(groupItem)
            groupItem.populate()
        self.addChild(groupsItem)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        stylesItem = QgsTreeItem(None, icon, "QGIS Styles")               
        stylesItem.setIcon(0, icon)
        styles = qgislayers.getAllLayers()
        for style in styles:
            styleItem = QgsStyleItem(style)            
            stylesItem.addChild(styleItem)
        self.addChild(stylesItem)        
            
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")        
        publishProjectAction = QtGui.QAction(icon, "Publish...", explorer)
        publishProjectAction.triggered.connect(lambda: self.publishProject(tree, explorer))
        publishProjectAction.setEnabled(len(explorer.catalogs())>0)        
        return [publishProjectAction]
                       
        
    def publishProject(self, tree, explorer):        
        layers = qgislayers.getAllLayers()                
        dlg = PublishProjectDialog(explorer.catalogs())
        dlg.exec_()   
        catalog  = dlg.catalog
        if catalog is None:
            return
        workspace = dlg.workspace
        groupName = dlg.groupName
        explorer.setProgressMaximum(len(layers), "Publish layers")
        progress = 0
        ogcat = OGCatalog(catalog)                    
        for layer in layers:
            explorer.setProgress(progress)                                         
            if not explorer.run(publishLayer,
                     None, 
                     [],
                     ogcat, layer, workspace, True):
                explorer.setProgress(0)
                return
            progress += 1                
            explorer.setProgress(progress)  
        explorer.resetActivity()
        groups = qgislayers.getGroups()
        for group in groups:
            names = [layer.name() for layer in groups[group]] 
            try:
                layergroup = catalog.create_layergroup(group, names, names)
                explorer.run(catalog.save, "Create layer group '" + group + "'", 
                     [], layergroup)
            except ConflictingDataError, e:
                explorer.setWarning(str(e))
        
        if groupName is not None:
            names = [layer.name() for layer in layers]      
            layergroup = catalog.create_layergroup(groupName, names, names)
            explorer.run(catalog.save, "Create global layer group", 
                     [], layergroup)                
        tree.findAllItems(catalog)[0].refreshContent(explorer)     
                                             
                    
class QgsLayerItem(QgsTreeItem): 
    def __init__(self, layer ): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, layer, icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)      
     
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/publish-to-geoserver.png")
        publishLayerAction = QtGui.QAction(icon, "Publish to GeoServer...", explorer)
        publishLayerAction.triggered.connect(lambda: self.publishLayer(tree, explorer)) 
        publishLayerAction.setEnabled(len(explorer.catalogs())>0)    
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/create-store-from-layer.png")   
        createStoreFromLayerAction= QtGui.QAction(icon, "Create store from layer...", explorer)
        createStoreFromLayerAction.triggered.connect(lambda: self.createStoreFromLayer(tree, explorer))
        createStoreFromLayerAction.setEnabled(len(explorer.catalogs())>0)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/postgis_import.png")
        importToPostGisAction = QtGui.QAction(icon, "Import into PostGIS...", explorer)
        importToPostGisAction.triggered.connect(lambda: self.importLayerToPostGis(tree, explorer))
        importToPostGisAction.setEnabled(len(explorer.pgDatabases())>0)
        
        return [publishLayerAction, createStoreFromLayerAction, importToPostGisAction]   
    
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
        return [publishLayersAction, createStoresFromLayersAction, importToPostGisAction] 
    
    def publishLayers(self, tree, explorer, selected):        
        layers = [item.element for item in selected]        
        dlg = PublishLayersDialog(explorer.catalogs(), layers)
        dlg.exec_()     
        toPublish  = dlg.topublish
        if toPublish is None:
            return
        explorer.setProgressMaximum(len(toPublish), "Publish layers")
        progress = 0        
        toUpdate = set();
        for layer, catalog, workspace in toPublish:
            explorer.setProgress(progress)            
            ogcat = OGCatalog(catalog)                 
            if explorer.run(publishLayer,
                     None,
                     [],
                     ogcat, layer, workspace, True):            
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
            explorer.setProgressMaximum(len(dlg.toImport), "Import layers to PostGIS")           
            for i, layer in enumerate(dlg.toImport):                
                explorer.run(dlg.connection.importFileOrLayer, 
                None,#"Import" + layer.name() + " into database " + dlg.connection.name,
                tree.findAllItems(schema),
                layer, dlg.schema, dlg.tablename, not dlg.add)
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
        toUpdate = set();
        for layer, catalog, workspace in toPublish:
            explorer.setProgress(progress)            
            ogcat = OGCatalog(catalog)                 
            explorer.run(ogcat.createStore,
                     None,#"Create store from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1
            toUpdate.add(tree.findAllItems(catalog))
            explorer.setProgress(progress)
        
        for item in toUpdate:
            item.refreshContent(explorer)
        explorer.resetActivity()
        
    def createStoreFromLayer(self, tree, explorer):
        dlg = PublishLayerDialog(explorer.catalogs())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = tree.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        explorer.run(ogcat.createStore,
                 "Create store from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, dlg.workspace, True)
                    
    def publishLayer(self, tree, explorer):
        dlg = PublishLayerDialog(explorer.catalogs())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = tree.findAllItems(cat)[0]                            
        explorer.run(publishLayer,
                 "Publish layer '" + self.element.name() + "'",
                 [catItem],
                 ogcat, self.element, dlg.workspace, True)

             
class QgsGroupItem(QgsTreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, group , icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        
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
        group = groups[groupname]     
        cat = selectCatalog(explorer.catalogs())
        if cat is None:
            return                            
        gslayers= [layer.name for layer in cat.get_layers()]
        missing = []        
        overwrite = bool(QSettings().value("/OpenGeo/Settings/GeoServer/OverwriteGroupLayers", True, bool)) 
        for layer in group:            
            if layer.name() not in gslayers or overwrite:
                missing.append(layer) 
        toUpdate = set();
        toUpdate.add(tree.findAllItems(cat)[0])
        
        if missing:
            catalogs = {k :v for k, v in explorer.catalogs().iteritems() if v == cat}
            dlg = PublishLayersDialog(catalogs, missing)
            dlg.exec_()     
            toPublish  = dlg.topublish
            if toPublish is None:
                return
            explorer.setProgressMaximum(len(toPublish), "Publish layers")
            progress = 0                    
            for layer, catalog, workspace in toPublish:
                explorer.setProgress(progress)            
                ogcat = OGCatalog(catalog)                 
                if not explorer.run(ogcat.publishLayer,
                         None,
                         [],
                         layer, workspace, True):
                    explorer.setProgress(0)
                    return
                progress += 1                
                explorer.setProgress(progress)
            explorer.resetActivity()      
        names = [layer.name() for layer in group]
        def _createGroup():      
            layergroup = cat.create_layergroup(groupname, names, names)
            cat.save(layergroup)
        explorer.run(_createGroup, "Create layer group from group '" + groupname + "'", 
                     toUpdate)    
       
               
class QgsStyleItem(QgsTreeItem): 
    def __init__(self, layer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeItem.__init__(self, layer, icon, "Style of layer '" + layer.name() + "'") 
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        
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
        dlg = PublishStyleDialog(explorer.catalogs().keys())
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