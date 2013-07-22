from PyQt4.QtCore import *
from qgis.core import *
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.layerdialog import PublishLayersDialog
from opengeo.gui.exploreritems import *

class ExplorerTreeWidget(QtGui.QTreeWidget):
    
    def __init__(self, explorer):         
        self.explorer = explorer
        QtGui.QTreeWidget.__init__(self, None) 
        
    def dropEvent(self, event):
        destinationItem=self.itemAt(event.pos())
        draggedTypes = {item.__class__ for item in self.selectedItems()}
        if len(draggedTypes) > 1:
            return
        draggedType = draggedTypes.pop()
        print "Dragging objects of type '" + str(draggedType) +"' into object of type '" + str(destinationItem.__class__) + "'"
        
        selected = self.selectedItems()
        self.explorer.progress.setMaximum(len(selected))
        i = 0
        toUpdate = set()
        for item in selected:            
            if isinstance(item, QgsLayerItem):
                if isinstance(destinationItem, GsWorkspaceItem):
                    self.publishLayer(item.element, destinationItem.element)
                    toUpdate.add(self.findAllItems(destinationItem.element.catalog)[0])
                elif isinstance(destinationItem, (GsResourceItem, GsStoreItem)):
                    self.publishLayer(item.element, destinationItem.element.workspace)
                    toUpdate.add(self.findAllItems(destinationItem.element.catalog)[0])
                elif isinstance(destinationItem, (GsWorkspacesItem, GsLayersItem, GsLayerItem, GsCatalogItem)):
                    catalog = destinationItem.parentCatalog()
                    workspace = self.getDefaultWorkspace(catalog)
                    if workspace is not None:
                        self.publishLayer(item.element, workspace)
                        toUpdate.add(self.findAllItems(catalog)[0])                    
            if isinstance(item, QgsGroupItem):
                if isinstance(destinationItem, (GsResourceItem, GsStoreItem, GsWorkspaceItem)):
                    self.publishGroup(item, destinationItem.element.catalog)
                    toUpdate.add(self.findAllItems(destinationItem.element.catalog)[0])                     
                elif isinstance(destinationItem, (GsGroupsItem, GsGroupItem, GsCatalogItem)):
                    catalog = destinationItem.parentCatalog()
                    workspace = self.getDefaultWorkspace(catalog)
                    self.publishGroup(item, catalog, workspace)
                    toUpdate.add(self.findAllItems(catalog)[0])                    
            elif isinstance(item, GsLayerItem):                    
                if isinstance(destinationItem, GsGroupItem):
                    self.addLayerToGroup(item.element, destinationItem)
                    toUpdate.add(destinationItem)                            
                if isinstance(destinationItem, GsLayerItem):
                    if isinstance(destinationItem.parent(), GsGroupItem):
                        destinationItem = destinationItem.parent()
                        self.addLayerToGroup(item.element, destinationItem)
                        toUpdate.add(destinationItem)
            elif isinstance(item, (GsStyleItem,QgsStyleItem)):
                if isinstance(destinationItem, GsLayerItem):                                            
                    self.addStyleToLayer(item, destinationItem)
                    toUpdate.add(destinationItem)                
                elif isinstance(destinationItem, GsStyleItem):
                    if isinstance(destinationItem.parent(), GsLayerItem):
                        destinationItem = destinationItem.parent()
                        self.addStyleToLayer(item, destinationItem)
                        toUpdate.add(destinationItem)
                    elif isinstance(destinationItem.parent(), GsStylesItem) and isinstance(item, QgsStyleItem):
                        self.publishStyle(item.element.name(), destinationItem.parent())                                                   
                elif isinstance(destinationItem, GsCatalogItem) and isinstance(item, QgsStyleItem):                    
                    self.publishStyle(item.element.name(), destinationItem)                           
            else:
                continue                                        
            i += 1
            self.explorer.progress.setValue(i)
        
        for item in toUpdate:
            item.refreshContent()        
        self.explorer.progress.setValue(0)
        event.acceptProposedAction()
        
    def getDefaultWorkspace(self, catalog):                            
        workspaces = catalog.get_workspaces()
        if workspaces:
            return catalog.get_default_workspace()
        else:
            return None
            
    def publishGroup(self, groupItem, catalog, workspace = None):        
        groupName = groupItem.element
        groups = qgislayers.getGroups()   
        group = groups[groupName]           
        gslayers= [layer.name for layer in catalog.get_layers()]
        missing = []         
        for layer in group:            
            if layer.name() not in gslayers:
                missing.append(layer)         
        if missing:
            self.explorer.progress.setMaximum(len(missing))
            progress = 0
            ogcat = OGCatalog(catalog)      
            if workspace:
                for layer in missing:
                    self.explorer.progress.setValue(progress)                                           
                    self.explorer.run(ogcat.publishLayer,
                             "Layer correctly published from layer '" + layer.name() + "'",
                             [],
                             layer, workspace, True)
                    progress += 1                                    
            else:
                catalogs = {k :v for k, v in self.explorer.catalogs.iteritems() if v == catalog}
                dlg = PublishLayersDialog(catalogs, missing)
                dlg.exec_()     
                toPublish  = dlg.topublish
                if toPublish is None:
                    return                                    
                for layer, catalog, workspace in toPublish:
                    self.explorer.progress.setValue(progress)            
                    ogcat = OGCatalog(catalog)                 
                    self.explorer.run(ogcat.publishLayer,
                             "Layer correctly published from layer '" + layer.name() + "'",
                             [],
                             layer, workspace, True)
                    progress += 1                
            self.explorer.progress.setValue(progress)  
        names = [layer.name() for layer in group]      
        layergroup = catalog.create_layergroup(groupName, names, names)
        self.explorer.run(catalog.save, "Layer group correctly created from group '" + groupName + "'", 
                 [], layergroup)               
        
    def publishStyle(self, layerName, catalogItem):
        ogcat = OGCatalog(catalogItem.element)
        toUpdate = []
        for idx in range(catalogItem.childCount()):
            subitem = catalogItem.child(idx)
            if isinstance(subitem, GsStylesItem):
                toUpdate.append(subitem)
                break                
        self.explorer.run(ogcat.publishStyle,
                 "Style correctly published from layer '" + layerName + "'",
                 toUpdate,
                 layerName, True, layerName)

    def publishLayer(self, layer, workspace):
        cat = workspace.catalog  
        ogcat = OGCatalog(cat)                                
        self.explorer.run(ogcat.publishLayer,
                 "Layer correctly published from layer '" + layer.name() + "'",
                 [],
                 layer, workspace, True)
        
    def addLayerToGroup(self, layer, groupItem):
        print "adding"
        group = groupItem.element
        styles = group.styles
        layers = group.layers
        if layer.name not in layers:
            layers.append(layer.name)
            styles.append(layer.default_style.name)
        group.dirty.update(layers = layers, styles = styles)
        self.explorer.run(layer.catalog.save,
                     "Group '" + group.name + "' correctly updated",
                     [groupItem],
                     group)
        
    def addStyleToLayer(self, styleItem, layerItem):
        catalog = layerItem.element.catalog  
        if isinstance(styleItem, QgsStyleItem):
            styleName = styleItem.element.name()
                       
            catalogItem = self.findAllItems(catalog)[0]
            self.publishStyle(styleName, catalogItem)     
            style = catalog.get_style(styleName)
        else:         
            style = styleItem.element            
        layer = layerItem.element
        styles = layer.styles                            
        styles.append(style)
        layer.styles = styles                        
        self.explorer.run(catalog.save, 
                 "Style '" + style.name + "' correctly added to layer '" + layer.name + "'",
                 [layerItem],
                 layer)                      
            
    def findAllItems(self, element):
        allItems = []
        iterator = QtGui.QTreeWidgetItemIterator(self)
        value = iterator.value()
        while value:
            if hasattr(value, 'element'):
                if hasattr(value.element, 'name') and hasattr(element, 'name'):
                    if  value.element.name == element.name and value.element.__class__ == element.__class__:
                        allItems.append(value)
                elif value.element == element:
                    allItems.append(value)                
            iterator += 1
            value = iterator.value()
        return allItems      
                     


                 
