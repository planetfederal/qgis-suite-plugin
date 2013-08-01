import os
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from opengeo.gui.exploreritems import TreeItem
from opengeo.qgis import layers as qgislayers
from opengeo.gui.styledialog import PublishStyleDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogselector import selectCatalog
from opengeo.gui.layerdialog import PublishLayersDialog, PublishLayerDialog
from opengeo.gui.projectdialog import PublishProjectDialog
                
class QgsProjectItem(TreeItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/qgis.png")
        TreeItem.__init__(self, None, icon, "QGIS project")        
                 
    def populate(self):                    
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        layersItem = TreeItem(None, icon, "Layers")        
        layersItem.setIcon(0, icon)
        layers = qgislayers.getAllLayers()
        for layer in layers:
            layerItem = QgsLayerItem(layer)            
            layersItem.addChild(layerItem)
        self.addChild(layersItem)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        groupsItem = TreeItem(None, icon, "Groups")        
        groups = qgislayers.getGroups()
        for group in groups:
            groupItem = QgsGroupItem(group)                                
            groupsItem.addChild(groupItem)
            groupItem.populate()
        self.addChild(groupsItem)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        stylesItem = TreeItem(None, icon, "Styles")               
        stylesItem.setIcon(0, icon)
        styles = qgislayers.getVectorLayers()
        for style in styles:
            styleItem = QgsStyleItem(style)            
            stylesItem.addChild(styleItem)
        self.addChild(stylesItem)        
            
    def contextMenuActions(self, explorer):
        self.explorer = explorer 
        publishProjectAction = QtGui.QAction("Publish...", explorer)
        publishProjectAction.triggered.connect(self.publishProject)
        publishProjectAction.setEnabled(len(self.explorer.tree.gsItem.catalogs())>0)        
        return [publishProjectAction]
                       
        
    def publishProject(self):        
        layers = qgislayers.getAllLayers()                
        dlg = PublishProjectDialog(self.explorer.tree.gsItem.catalogs())
        dlg.exec_()     
        catalog  = dlg.catalog
        if catalog is None:
            return
        workspace = dlg.workspace
        groupName = dlg.groupName
        self.explorer.progress.setMaximum(len(layers))
        progress = 0                    
        for layer in layers:
            self.explorer.progress.setValue(progress)            
            ogcat = OGCatalog(catalog)                 
            if not self.explorer.run(ogcat.publishLayer,
                     "Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True):
                self.explorer.progress.setValue(0)
                return
            progress += 1                
        self.explorer.progress.setValue(progress)  
        
        names = [layer.name() for layer in layers]      
        layergroup = catalog.create_layergroup(groupName, names, names)
        self.explorer.run(catalog.save, "Layer group correctly created from project", 
                 [], layergroup)                
        self.explorer.tree.findAllItems(catalog)[0].refreshContent()
        self.explorer.progress.setValue(0)                                                 
                    
class QgsLayerItem(TreeItem): 
    def __init__(self, layer ): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, layer, icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)      
     
    def contextMenuActions(self, explorer):
        self.explorer = explorer 
        publishLayerAction = QtGui.QAction("Publish...", explorer)
        publishLayerAction.triggered.connect(self.publishLayer) 
        publishLayerAction.setEnabled(len(self.explorer.tree.gsItem.catalogs())>0)       
        createStoreFromLayerAction= QtGui.QAction("Create store from layer...", explorer)
        createStoreFromLayerAction.triggered.connect(self.createStoreFromLayer)
        createStoreFromLayerAction.setEnabled(len(self.explorer.tree.gsItem.catalogs())>0)
        return [publishLayerAction, createStoreFromLayerAction]   
    
    def multipleSelectionContextMenuActions(self, explorer, selected):
        self.explorer = explorer        
        publishLayersAction = QtGui.QAction("Publish...", explorer)
        publishLayersAction.triggered.connect(lambda: self.publishLayers(selected))        
        createStoresFromLayersAction= QtGui.QAction("Create stores from layers...", explorer)
        createStoresFromLayersAction.triggered.connect(lambda: self.createStoresFromLayers(selected))
        return [publishLayersAction, createStoresFromLayersAction] 
    
    def publishLayers(self, selected):        
        layers = [item.element for item in selected]        
        dlg = PublishLayersDialog(self.explorer.tree.gsItem.catalogs(), layers)
        dlg.exec_()     
        toPublish  = dlg.topublish
        if toPublish is None:
            return
        self.explorer.progress.setMaximum(len(toPublish))
        progress = 0        
        toUpdate = set();
        for layer, catalog, workspace in toPublish:
            self.explorer.progress.setValue(progress)            
            ogcat = OGCatalog(catalog)                 
            self.explorer.run(ogcat.publishLayer,
                     "Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1
            toUpdate.add(self.explorer.tree.findAllItems(catalog)[0])
        self.explorer.progress.setValue(progress)
        
        for item in toUpdate:
            item.refreshContent()
        self.explorer.progress.setValue(0)        
                           

        
    def createStoresFromLayers(self, selected):        
        layers = [item.element for item in selected]        
        dlg = PublishLayersDialog(self.explorer.tree.gsItem.catalogs(), layers)
        dlg.exec_()     
        toPublish  = dlg.topublish
        if toPublish is None:
            return
        self.explorer.progress.setMaximum(len(toPublish))
        progress = 0        
        toUpdate = set();
        for layer, catalog, workspace in toPublish:
            self.explorer.progress.setValue(progress)            
            ogcat = OGCatalog(catalog)                 
            self.explorer.run(ogcat.createStore,
                     "Store correctly created from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1
            toUpdate.add(self.explorer.tree.findAllItems(catalog))
        self.explorer.progress.setValue(progress)
        
        for item in toUpdate:
            item.refreshContent()
        self.explorer.progress.setValue(0)
        
    def createStoreFromLayer(self):
        dlg = PublishLayerDialog(self.explorer.tree.gsItem.catalogs())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = self.explorer.tree.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        self.explorer.run(ogcat.createStore,
                 "Store correctly created from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, dlg.workspace, True)
                    
    def publishLayer(self):
        dlg = PublishLayerDialog(self.explorer.tree.gsItem.catalogs())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = self.explorer.tree.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        self.explorer.run(ogcat.publishLayer,
                 "Layer correctly published from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, dlg.workspace, True)

             
class QgsGroupItem(TreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, group , icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        
    def populate(self):            
        grouplayers = qgislayers.getGroups()[self.element]
        for layer in grouplayers:
            layerItem = QgsLayerItem(layer)                                
            self.addChild(layerItem)

    def contextMenuActions(self, explorer):
        self.explorer = explorer            
        publishGroupAction = QtGui.QAction("Publish...", explorer)
        publishGroupAction.triggered.connect(self.publishGroup)
        publishGroupAction.setEnabled(len(self.explorer.tree.gsItem.catalogs())>0)
        return[publishGroupAction]  
        
    def publishGroup(self):
        groupname = self.element
        groups = qgislayers.getGroups()   
        group = groups[groupname]     
        cat = selectCatalog(self.explorer.tree.gsItem.catalogs())
        if cat is None:
            return                            
        gslayers= [layer.name for layer in cat.get_layers()]
        missing = []         
        for layer in group:            
            if layer.name() not in gslayers:
                missing.append(layer) 
        toUpdate = set();
        toUpdate.add(self.explorer.tree.findAllItems(cat)[0])
        if missing:
            catalogs = {k :v for k, v in self.explorer.tree.gsItem.catalogs().iteritems() if v == cat}
            dlg = PublishLayersDialog(catalogs, missing)
            dlg.exec_()     
            toPublish  = dlg.topublish
            if toPublish is None:
                return
            self.explorer.progress.setMaximum(len(toPublish))
            progress = 0                    
            for layer, catalog, workspace in toPublish:
                self.explorer.progress.setValue(progress)            
                ogcat = OGCatalog(catalog)                 
                if not self.explorer.run(ogcat.publishLayer,
                         "Layer correctly published from layer '" + layer.name() + "'",
                         [],
                         layer, workspace, True):
                    self.explorer.progress.setValue(0)
                    return
                progress += 1                
            self.explorer.progress.setValue(progress)  
        names = [layer.name() for layer in group]      
        layergroup = cat.create_layergroup(groupname, names, names)
        self.explorer.run(cat.save, "Layer group correctly created from group '" + groupname + "'", 
                 [], layergroup)        
        for item in toUpdate:
            item.refreshContent()
        self.explorer.progress.setValue(0)                       
               
class QgsStyleItem(TreeItem): 
    def __init__(self, layer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeItem.__init__(self, layer, icon, "Style of layer '" + layer.name() + "'") 
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        
    def contextMenuActions(self, explorer):
        self.explorer = explorer  
        publishStyleAction = QtGui.QAction("Publish...", explorer)
        publishStyleAction.triggered.connect(self.publishStyle)
        publishStyleAction.setEnabled(self.explorer.tree.gsItem.catalogs())
        return [publishStyleAction]    
        
    def publishStyle(self):
        dlg = PublishStyleDialog(self.explorer.tree.gsItem.catalogs().keys())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = self.explorer.tree.gsItem.catalogs()[dlg.catalog]  
        ogcat = OGCatalog(cat)
        catItem = self.explorer.tree.findAllItems(cat)[0]
        toUpdate = [catItem.stylesItem]                        
        self.explorer.run(ogcat.publishStyle,
                 "Style correctly published from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, True, dlg.name)              