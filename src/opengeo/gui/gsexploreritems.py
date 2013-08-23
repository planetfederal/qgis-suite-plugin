import os
from qgis.core import *
from PyQt4 import QtGui,QtCore, QtWebKit
from PyQt4.QtCore import *
from opengeo.qgis import layers as qgislayers
from opengeo.geoserver.store import DataStore
from opengeo.geoserver.resource import Coverage, FeatureType
from opengeo.geoserver.gwc import Gwc, GwcLayer, SeedingStatusParsingError
from opengeo.gui.catalogdialog import DefineCatalogDialog
from opengeo.geoserver.style import Style
from opengeo.geoserver.layer import Layer
from opengeo.gui.styledialog import AddStyleToLayerDialog, StyleFromLayerDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.exploreritems import TreeItem
from opengeo.gui.groupdialog import LayerGroupDialog
from opengeo.gui.workspacedialog import DefineWorkspaceDialog
from opengeo.gui.gwclayer import SeedGwcLayerDialog, EditGwcLayerDialog
from opengeo.geoserver.layergroup import UnsavedLayerGroup
from opengeo.gui.qgsexploreritems import QgsLayerItem, QgsGroupItem,\
    QgsStyleItem
from opengeo.geoserver.catalog import FailedRequestError
from opengeo.gui.pgexploreritems import PgTableItem
import traceback
from opengeo.geoserver.wps import Wps
from opengeo.gui.crsdialog import CrsSelectionDialog
from opengeo.geoserver.settings import Settings
from opengeo.gui.parametereditor import ParameterEditor
from opengeo.gui.sldeditor import SldEditorDialog

class GsTreeItem(TreeItem):
    
    def parentCatalog(self):   
        if hasattr(self, 'catalog') and self.catalog is not None:
            return self.catalog     
        item  = self            
        while item is not None:                    
            if isinstance(item, GsCatalogItem):
                return item.element    
            if hasattr(item, 'catalog') and item.catalog is not None:  
                return item.catalog                    
            item = item.parent()            
        return None   
    
    def parentWorkspace(self):        
        item  = self            
        while item is not None:                    
            if isinstance(item, GsWorkspaceItem):
                return item.element                           
            item = item.parent()            
        return None   
                 
    def getDefaultWorkspace(self):                            
        workspaces = self.parentCatalog().get_workspaces()
        if workspaces:
            return self.parentCatalog().get_default_workspace()
        else:
            return None  
        
    def deleteElements(self, selected, tree, explorer):                
        elements = []
        unused = []
        for item in selected:
            elements.append(item.element)
            if isinstance(item, GsStoreItem):
                for idx in range(item.childCount()):
                    subitem = item.child(idx)
                    elements.insert(0, subitem.element)
            elif isinstance(item, GsLayerItem):
                uniqueStyles = self.uniqueStyles(item.element)
                for style in uniqueStyles:
                    if style.name == item.element.name:
                        unused.append(style)      
        toUpdate = set(item.parent() for item in selected)                
        explorer.progress.setMaximum(len(elements))
        progress = 0        
        dependent = self.getDependentElements(elements)
                
        if dependent:
            msg = "The following elements depend on the elements to delete\nand will be deleted as well:\n\n"
            for e in dependent:
                msg += "-" + e.name + "(" + e.__class__.__name__ + ")\n\n"
            msg += "Do you really want to delete all these elements?"                   
            reply = QtGui.QMessageBox.question(None, "Delete confirmation",
                                               msg, QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
            toDelete = set()
            for e in dependent:                
                items = tree.findAllItems(e);                
                toUpdate.update(set(item.parent() for item in items))
                toDelete.update(items)
            toUpdate = toUpdate - toDelete
        
                
        unusedToUpdate = set() 
        for e in unused:                
            items = tree.findAllItems(e); 
            unusedToUpdate.add(item.parent())                       
        toUpdate.update(unusedToUpdate)
        
        elements[0:0] = dependent 
        elements.extend(unused)      
        for element in elements:
            explorer.progress.setValue(progress)    
            if isinstance(element, GwcLayer):
                explorer.run(element.delete,
                     "Delete " + element.__class__.__name__ + " '" + element.name + "'",
                     [])                      
            else:                                     
                explorer.run(element.catalog.delete,
                     "Delete " + element.__class__.__name__ + " '" + element.name + "'",
                     [], 
                     element, isinstance(element, Style))  
            progress += 1
        explorer.progress.setValue(progress)
        for item in toUpdate:
            if item is not None:
                item.refreshContent()
        if None in toUpdate:
            explorer.refreshContent()
        explorer.progress.setValue(0)
    
    def uniqueStyles(self, layer):
        '''returns the styles used by a layer that are not used by any other layer'''
        unique = []
        allUsedStyles = set()
        catalog = layer.catalog
        layers = catalog.get_layers()
        for lyr in layers:
            if lyr.name == layer.name:
                continue
            for style in lyr.styles:
                allUsedStyles.add(style.name)
                if lyr.default_style is not None:
                    allUsedStyles.add(lyr.default_style.name)
        for style in layer.styles:
            if style.name not in allUsedStyles:
                unique.append(style)
        if layer.default_style is not None and layer.default_style not in allUsedStyles:
            unique.append(layer.default_style)
        return unique
            
    def getDependentElements(self, elements):
        dependent = []
        for element in elements:
            if isinstance(element, Layer):
                groups = element.catalog.get_layergroups()
                for group in groups:                    
                    for layer in group.layers:
                        if layer == element.name:
                            dependent.append(group)
                            break                    
            elif isinstance(element, (FeatureType, Coverage)):
                layers = element.catalog.get_layers()
                for layer in layers:
                    if layer.resource.name == element.name:
                        dependent.append(layer)     
            elif isinstance(element, Style):
                layers = element.catalog.get_layers()                
                for layer in layers:
                    if layer.default_style.name == element.name:
                        dependent.append(layer)                         
                    else:
                        for style in layer.styles:                            
                            if style.name == element.name:
                                dependent.append(layer)
                                break
                                                                                    
        if dependent:
            subdependent = self.getDependentElements(dependent)
            if subdependent:
                dependent[0:0] = subdependent
        return dependent
                                     
    
class GsCatalogsItem(GsTreeItem):    
    def __init__(self): 
        self._catalogs = {}
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")        
        GsTreeItem.__init__(self, None, icon, "GeoServer catalogs")        
                 
    def populate(self):
        for name, catalog in self._catalogs.iteritems():                    
            item = self.getGeoServerCatalogItem(catalog, name)
            self.addChild(item)

    def contextMenuActions(self, tree, explorer):        
        createCatalogAction = QtGui.QAction("New catalog...", explorer)
        createCatalogAction.triggered.connect(lambda: self.addGeoServerCatalog(explorer))
        return [createCatalogAction]
                    
    def addGeoServerCatalog(self, explorer):         
        dlg = DefineCatalogDialog()
        dlg.exec_()
        cat = dlg.getCatalog()        
        if cat is not None:   
            name = dlg.getName()
            i = 2
            while name in self._catalogs.keys():
                name = dlg.getName() + "_" + str(i)
                i += 1                                 
            item = self.getGeoServerCatalogItem(cat, name, explorer)
            if item is not None:
                self._catalogs[name] = cat
                self.addChild(item)
                self.setExpanded(True)
        
        
    def getGeoServerCatalogItem(self, cat, name, explorer):    
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        try:    
            geoserverItem = GsCatalogItem(cat, name)
            geoserverItem.populate()
            QtGui.QApplication.restoreOverrideCursor()
            explorer.setInfo("Catalog '" + name + "' correctly created")
            return geoserverItem
        except Exception, e:   
            traceback.print_exc()         
            QtGui.QApplication.restoreOverrideCursor()
            explorer.setInfo("Could not create catalog:" + str(e), 1)                          
            
class GsLayersItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        GsTreeItem.__init__(self, None, icon, "Layers")
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled) 
            
    def populate(self):
        layers = self.catalog.get_layers()
        for layer in layers:
            layerItem = GsLayerItem(layer)            
            layerItem.populate()    
            self.addChild(layerItem) 
        self.sortChildren(0, Qt.AscendingOrder)                  
    
    def acceptDroppedItem(self, tree, explorer, item):            
        if isinstance(item, GsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate  
        elif isinstance(item, QgsGroupItem):                
            catalog = self.parentCatalog()
            if catalog is None:
                return
            workspace = self.parentWorkspace()
            if workspace is None:
                workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return explorer.tree.findAllItems(catalog)
        elif isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate  
                        
class GsGroupsItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        GsTreeItem.__init__(self, None, icon, "Groups")           
        
    def populate(self):
        groups = self.catalog.get_layergroups()
        for group in groups:
            groupItem = GsGroupItem(group)
            groupItem.populate()                                
            self.addChild(groupItem)    
            
    def acceptDroppedItem(self, tree, explorer, item):                    
        if isinstance(item, QgsGroupItem):                
            catalog = self.parentCatalog()
            if catalog is None:
                return
            workspace = self.parentWorkspace()
            if workspace is None:
                workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return explorer.tree.findAllItems(catalog)       
    
    def contextMenuActions(self, tree, explorer):            
        createGroupAction = QtGui.QAction("New group...", explorer)
        createGroupAction.triggered.connect(lambda: self.createGroup(explorer))
        return [createGroupAction]
    
    def createGroup(self, explorer):
        dlg = LayerGroupDialog(self.parentCatalog())
        dlg.exec_()
        group = dlg.group
        if group is not None:
            explorer.run(self.parentCatalog().save,
                     "Create group '" + group.name + "'",
                     [self],
                     group)
     
        
class GsWorkspacesItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/workspace.png")
        GsTreeItem.__init__(self, None, icon, "Workspaces")  
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)        
    
    def populate(self):
        cat = self.parentCatalog()
        try:
            defaultWorkspace = cat.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text
        except:
            defaultName = None             
        workspaces = cat.get_workspaces()
        for workspace in workspaces:
            workspaceItem = GsWorkspaceItem(workspace, workspace.name == defaultName)
            workspaceItem.populate()
            self.addChild(workspaceItem) 
    
    def acceptDroppedItem(self, tree, explorer, item):
        if isinstance(item, QgsGroupItem):                
            catalog = self.parentCatalog()
            if catalog is None:
                return
            workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return explorer.tree.findAllItems(catalog)
        elif isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate   
        elif isinstance(item, PgTableItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedTable(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate        

    def startDropEvent(self):
        self.uris = []        
        
    def acceptDroppedUri(self, explorer, uri):        
        self.uris.append(uri) 
    
    def finishDropEvent(self, explorer):        
        if self.uris:
            catalog = self.parentCatalog()
            files = []
            for uri in self.uris:
                try:
                    files.append(uri.split(":",3)[-1])
                except Exception, e:                    
                    pass            
            workspace = self.getDefaultWorkspace()                            
            for i, filename in enumerate(files):
                explorer.progress.setValue(i)
                layerName = QtCore.QFileInfo(filename).completeBaseName()
                layer = QgsVectorLayer(filename, layerName, "ogr")    
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    layer.deleteLater()
                    explorer.setInfo("Error reading file {} or it is not a valid vector layer file".format(filename), 1)                                
                else:
                    publishDraggedLayer(explorer, layer, workspace)
            return [explorer.tree.findAllItems(catalog)[0]]
        else:
            return []
                            
    def contextMenuActions(self, tree, explorer):        
        createWorkspaceAction = QtGui.QAction("New workspace...", explorer)
        createWorkspaceAction.triggered.connect(lambda: self.createWorkspace(explorer))
        return [createWorkspaceAction]
    
    def createWorkspace(self, explorer):
        dlg = DefineWorkspaceDialog() 
        dlg.exec_()            
        if dlg.name is not None:
            explorer.run(self.parentCatalog().create_workspace, 
                    "Create workspace '" + dlg.name + "'",
                    [self],
                    dlg.name, dlg.uri)
                 
class GsStylesItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        GsTreeItem.__init__(self, None, icon, "Styles")
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled) 
                    
    def populate(self):
        styles = self.parentCatalog().get_styles()
        for style in styles:
            styleItem = GsStyleItem(style, False)                
            self.addChild(styleItem)

    def acceptDroppedItem(self, tree, explorer, item):
        if isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate  
        
    def contextMenuActions(self, tree, explorer):        
        createStyleFromLayerAction = QtGui.QAction("New style from QGIS layer...", explorer)
        createStyleFromLayerAction.triggered.connect(lambda: self.createStyleFromLayer(explorer))
        return [createStyleFromLayerAction] 
           
    
    def createStyleFromLayer(self, explorer):  
        dlg = StyleFromLayerDialog(explorer.catalogs().keys())
        dlg.exec_()      
        if dlg.layer is not None:
            ogcat = OGCatalog(explorer.catalogs()[dlg.catalog])        
            explorer.run(ogcat.publishStyle, 
                     "Create style from layer '" + dlg.layer + "'",
                     [self],
                     dlg.layer, True, dlg.name)


class GsCatalogItem(GsTreeItem): 
    def __init__(self, catalog, name): 
        self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
        GsTreeItem.__init__(self, catalog, icon, name) 
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled) 
        
    def populate(self):        
        self.workspacesItem = GsWorkspacesItem(self.catalog)                              
        self.addChild(self.workspacesItem)  
        self.workspacesItem.populate()
        self.layersItem = GsLayersItem(self.catalog)                                      
        self.addChild(self.layersItem)
        self.layersItem.populate()
        self.groupsItem = GsGroupsItem(self.catalog)                                    
        self.addChild(self.groupsItem)
        self.groupsItem.populate()
        self.stylesItem = GsStylesItem(self.catalog)                        
        self.addChild(self.stylesItem)
        self.stylesItem.populate()      
        self.gwcItem = GwcLayersItem(self.catalog)                        
        self.addChild(self.gwcItem)
        self.gwcItem.populate()
        self.wpsItem = GsProcessesItem(self.catalog)                        
        self.addChild(self.wpsItem)
        self.wpsItem.populate()
        self.settingsItem = GsSettingsItem(self.catalog)                        
        self.addChild(self.settingsItem)
        

    def acceptDroppedItem(self, tree, explorer, item):
        if isinstance(item, QgsStyleItem):                    
            publishDraggedStyle(item.element.name(), self) 
            return [self]   
        elif isinstance(item, QgsGroupItem):                
            catalog = self.element                        
            workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return [self]
        elif isinstance(item, QgsLayerItem):
            catalog = self.element
            workspace = self.getDefaultWorkspace()                        
            publishDraggedLayer(explorer, item.element, workspace)            
            return [self]
        
    def contextMenuActions(self, tree, explorer):        
        removeCatalogAction = QtGui.QAction("Remove", explorer)
        removeCatalogAction.triggered.connect(lambda: self.removeCatalog(explorer))
        return[removeCatalogAction] 
        
    def removeCatalog(self, explorer):
        del explorer.catalogs()[self.text(0)]
        parent = self.parent()        
        parent.takeChild(parent.indexOfChild(self))   
        
    def _getDescriptionHtml(self, tree, explorer):                        
        return self.catalog.about()       
           
                                
class GsLayerItem(GsTreeItem): 
    def __init__(self, layer):
        self.catalog = layer.catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        GsTreeItem.__init__(self, layer, icon, layer.resource.title)  
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 
                      | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled)       
                
    def populate(self):
        layer = self.element
        for style in layer.styles:
            styleItem = GsStyleItem(style, False)
            self.addChild(styleItem)
        if layer.default_style is not None:
            styleItem = GsStyleItem(layer.default_style, True)                    
            self.addChild(styleItem)  
            
    def acceptDroppedItem(self, tree, explorer, item):
        if isinstance(item, (GsStyleItem, QgsStyleItem)):                                                        
            addDraggedStyleToLayer(explorer, item, self)
            return [self] 
        elif isinstance(item, GsLayerItem):
            destinationItem = self.parent()
            toUpdate = []
            if isinstance(destinationItem, GsGroupItem):
                addDraggedLayerToGroup(explorer, item.element, destinationItem)
                toUpdate.append(destinationItem)
            return toUpdate
        elif isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate  
    
    def _getDescriptionHtml(self, tree, explorer):                        
        html = u'<div style="background-color:#ffffcc;"><h1>&nbsp; ' + self.text(0) + ' (GeoServer layer)</h1></div></br>'  
        html += '<p><h3><b>Properties</b></h3></p><ul>'
        html += '<li><b>Name: </b>' + str(self.element.name) + '</li>\n'
        html += '<li><b>Title: </b>' + str(self.element.resource.title) + ' &nbsp;<a href="modify:title">Modify</a></li>\n'     
        html += '<li><b>Abstract: </b>' + str(self.element.resource.abstract) + ' &nbsp;<a href="modify:abstract">Modify</a></li>\n'
        html += ('<li><b>SRS: </b>' + str(self.element.resource.projection) + ' &nbsp;<a href="modify:srs">Modify</a> '
                                    '&nbsp;<a href="modify:setinproject">Set as project SRS</a></li>\n')        
        bbox = self.element.resource.latlon_bbox
        html += '<li><b>Bounding box (lat/lon): </b> &nbsp;<a href="modify:zoomtobbox">Zoom to this bbox</a></li>\n<ul>'        
        html += '<li> N:' + str(bbox[3]) + '</li>'
        html += '<li> S:' + str(bbox[2]) + '</li>'
        html += '<li> E:' + str(bbox[0]) + '</li>'
        html += '<li> W:' + str(bbox[1]) + '</li>'
        html += '</ul>'                 
        html += '</ul>'
        actions = self.contextMenuActions(tree, explorer)
        html += "<p><h3><b>Available actions</b></h3></p><ul>"
        for action in actions:
            if action.isEnabled():
                html += '<li><a href="' + action.text() + '">' + action.text() + '</a></li>\n'
        html += '</ul>'
        return html 
    
    def linkClicked(self, tree, explorer, url):
        actionName = url.toString()
        if actionName == 'modify:title':
            text, ok = QtGui.QInputDialog.getText(None, "New title", "Enter new title", text=self.element.resource.title)
            if ok:                
                r = self.element.resource
                r.dirty['title'] = text                                 
                explorer.run(self.catalog.save, "Update layer title", [], r)            
        if actionName == 'modify:abstract':
            text, ok = QtGui.QInputDialog.getText(None, "New abstract", "Enter new abstract", text=self.element.resource.abstract)
            if ok:
                r = self.element.resource
                r.dirty['abstract'] = text                                 
                explorer.run(self.catalog.save, "Update layer abstract", [], r) 
        if actionName == 'modify:srs':
            dlg = CrsSelectionDialog()
            dlg.exec_()
            if dlg.authid is not None:
                r = self.element.resource
                r.dirty['srs'] = text                                 
                explorer.run(self.catalog.save, "Update layer srs", [], r) 
        actions = self.contextMenuActions(tree, explorer)
        for action in actions:
            if action.text() == actionName:
                action.trigger()
                return 
                
    def contextMenuActions(self, tree, explorer):        
        actions = []
        if isinstance(self.parent(), GsGroupItem):
            layers = self.parent().element.layers
            count = len(layers)
            idx = layers.index(self.element.name)
            removeLayerFromGroupAction = QtGui.QAction("Remove layer from group", explorer)            
            removeLayerFromGroupAction.setEnabled(count > 1)
            removeLayerFromGroupAction.triggered.connect(lambda: self.removeLayerFromGroup(explorer))
            actions.append(removeLayerFromGroupAction)                                                
            moveLayerUpInGroupAction = QtGui.QAction("Move up", explorer)            
            moveLayerUpInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerUpInGroupAction.triggered.connect(lambda: self.moveLayerUpInGroup(explorer))
            actions.append(moveLayerUpInGroupAction)
            moveLayerDownInGroupAction = QtGui.QAction("Move down", explorer)            
            moveLayerDownInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerDownInGroupAction.triggered.connect(lambda: self.moveLayerDownInGroup(explorer))
            actions.append(moveLayerDownInGroupAction)
            moveLayerToFrontInGroupAction = QtGui.QAction("Move to front", explorer)            
            moveLayerToFrontInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerToFrontInGroupAction.triggered.connect(lambda: self.moveLayerToFrontInGroup(explorer))
            actions.append(moveLayerToFrontInGroupAction)
            moveLayerToBackInGroupAction = QtGui.QAction("Move to back", explorer)            
            moveLayerToBackInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerToBackInGroupAction.triggered.connect(lambda: self.moveLayerToBackInGroup(explorer))
            actions.append(moveLayerToBackInGroupAction)
        else:
            addStyleToLayerAction = QtGui.QAction("Add style to layer...", explorer)
            addStyleToLayerAction.triggered.connect(lambda: self.addStyleToLayer(explorer))                    
            actions.append(addStyleToLayerAction)   
            deleteLayerAction = QtGui.QAction("Delete", None)
            deleteLayerAction.triggered.connect(lambda: self.deleteLayer(tree, explorer))
            actions.append(deleteLayerAction)                                
            addLayerAction = QtGui.QAction("Add to current QGIS project", explorer)
            addLayerAction.triggered.connect(lambda: self.addLayerToProject(explorer))
            actions.append(addLayerAction)    
            
        return actions
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):        
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        createGroupAction = QtGui.QAction("Create group...", explorer)
        createGroupAction.triggered.connect(lambda: self.createGroupFromLayers(selected, tree, explorer))        
        return [deleteSelectedAction, createGroupAction]
                 
            
    def createGroupFromLayers(self, selected, tree, explorer):        
        name, ok = QtGui.QInputDialog.getText(None, "Group name", "Enter the name of the group to create")        
        if not ok:
            return
        catalog = self.element.catalog
        catalogItem = tree.findAllItems(catalog)[0]
        if catalogItem is not None:
            groupsItem = catalogItem.groupsItem
        else:
            groupItem = None
        layers = [item.element for item in selected]
        styles = [layer.default_style.name for layer in layers]
        layerNames = [layer.name for layer in layers]
        #TODO calculate bounds
        bbox = None
        group =  UnsavedLayerGroup(catalog, name, layerNames, styles, bbox)
                
        explorer.run(self.parentCatalog().save,
                     "Create group '" + name + "'",
                     [groupsItem],
                     group)
                    
    def deleteLayer(self, tree, explorer):
        self.deleteElements([self], tree, explorer)
            
    def removeLayerFromGroup(self, explorer):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        del layers[idx]
        del styles[idx]
        group.dirty.update(layers = layers, styles = styles)
        explorer.run(self.parentCatalog().save, 
                 "Remove layer '" + self.element.name + "' from group '" + group.name +"'",
                 [self.parent()],
                 group)

    def moveLayerDownInGroup(self, explorer):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        tmp = layers [idx + 1]
        layers[idx + 1] = layers[idx]
        layers[idx] = tmp  
        tmp = styles [idx + 1]
        styles[idx + 1] = styles[idx]
        styles[idx] = tmp          
        group.dirty.update(layers = layers, styles = styles)
        explorer.run(self.parentCatalog().save, 
                 "Move layer '" + self.element.name + "' down in group '" + group.name +"'",
                 [self.parent()],
                 group)        
    
    def moveLayerToFrontInGroup(self, explorer):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        tmp = layers[idx]
        del layers[idx]
        layers.insert(0, tmp)        
        tmp = styles [idx]
        del styles[idx]
        styles.insert(0, tmp)          
        group.dirty.update(layers = layers, styles = styles)
        explorer.run(self.parentCatalog().save, 
                 "Move layer '" + self.element.name + "' to front in group '" + group.name +"'",
                 [self.parent()],
                 group)
    
    def moveLayerToBackInGroup(self, explorer):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        tmp = layers[idx]
        del layers[idx]
        layers.append(tmp)        
        tmp = styles [idx]
        del styles[idx]
        styles.append(tmp)          
        group.dirty.update(layers = layers, styles = styles)
        explorer.run(self.parentCatalog().save, 
                 "Move layer '" + self.element.name + "' to back in group '" + group.name +"'",
                 [self.parent()],
                 group)
                     
    def moveLayerUpInGroup(self, explorer):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        tmp = layers [idx - 1]
        layers[idx - 1] = layers[idx]
        layers[idx] = tmp  
        tmp = styles [idx - 1]
        styles[idx - 1] = styles[idx]
        styles[idx] = tmp          
        group.dirty.update(layers = layers, styles = styles)
        explorer.run(self.parentCatalog().save, 
                 "Move layer '" + self.element.name + "' up in group '" + group.name +"'",
                 [self.parent()],
                 group)    
        
            
    def addStyleToLayer(self, explorer):
        cat = self.parentCatalog()
        dlg = AddStyleToLayerDialog(cat)
        dlg.exec_()
        if dlg.style is not None:
            layer = self.element
            styles = layer.styles            
            if dlg.default:
                default = layer.default_style
                styles.append(default)
                layer.styles = styles
                layer.default_style = dlg.style                 
            else:
                styles.append(dlg.style)
                layer.styles = styles 
            explorer.run(cat.save, 
                     "Add style '" + dlg.style.name + "' to layer '" + layer.name + "'",
                     [self],
                     layer)  
            
    def addLayerToProject(self, explorer):
        #Using threads here freezes the QGIS GUI
        cat = OGCatalog(self.parentCatalog()) 
        cat.addLayerToProject(self.element.name) 
        explorer.setInfo("Layer '" + self.element.name + "' correctly added to QGIS project")                        

class GsGroupItem(GsTreeItem): 
    def __init__(self, group):
        self.catalog = group.catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        GsTreeItem.__init__(self, group, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 
                      | QtCore.Qt.ItemIsDropEnabled)  
        
    def populate(self):
        layers = self.element.catalog.get_layers()
        layersDict = {layer.name : layer for layer in layers}
        groupLayers = self.element.layers
        if groupLayers is None:
            return
        for layer in groupLayers:
            if ':' in layer:
                layer = layer.split(':')[1]
            layerItem = GsLayerItem(layersDict[layer])                          
            self.addChild(layerItem)
            
            
    def acceptDroppedItem(self, tree, explorer, item):                        
        if isinstance(item, GsLayerItem):
            addDraggedLayerToGroup(explorer, item.element, self)
            return [self]            
            
    def contextMenuActions(self, tree, explorer):
        editLayerGroupAction = QtGui.QAction("Edit...", explorer)
        editLayerGroupAction.triggered.connect(lambda: self.editLayerGroup(explorer))             
        deleteLayerGroupAction = QtGui.QAction("Delete", explorer)
        deleteLayerGroupAction.triggered.connect(lambda: self.deleteLayerGroup(tree, explorer))
        return [editLayerGroupAction, deleteLayerGroupAction]
       
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):        
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    
    def deleteLayerGroup(self, tree, explorer):
        self.deleteElements([self], tree, explorer);
        
    def editLayerGroup(self, explorer):
        cat = self.parentCatalog()        
        dlg = LayerGroupDialog(cat, self.element)
        dlg.exec_()
        group = dlg.group
        if group is not None:
            explorer.run(cat.save, "Edit layer group '" + self.element.name + "'", 
                              [self], 
                              group)   
    
                
            

class GsStyleItem(GsTreeItem): 
    def __init__(self, style, isDefault): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        name = style.name if not isDefault else style.name + " [default style]"
        GsTreeItem.__init__(self, style, icon, name)
        self.isDefault = isDefault     
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)        
        
    def contextMenuActions(self, tree, explorer):   
        actions = []
        if isinstance(self.parent(), GsLayerItem):
            setAsDefaultStyleAction = QtGui.QAction("Set as default style", explorer)
            setAsDefaultStyleAction.triggered.connect(lambda: self.setAsDefaultStyle(tree, explorer))
            setAsDefaultStyleAction.setEnabled(not self.isDefault)
            actions.append(setAsDefaultStyleAction)  
            removeStyleFromLayerAction = QtGui.QAction("Remove style from layer", explorer)
            removeStyleFromLayerAction.triggered.connect(lambda: self.removeStyleFromLayer(tree, explorer))
            removeStyleFromLayerAction.setEnabled(not self.isDefault)            
            actions.append(removeStyleFromLayerAction)                           
        else:                      
            deleteStyleAction = QtGui.QAction("Delete", explorer)
            deleteStyleAction.triggered.connect(lambda: self.deleteStyle(tree, explorer))
            actions.append(deleteStyleAction)
        editStyleAction = QtGui.QAction("Edit SLD...", explorer)
        editStyleAction.triggered.connect(lambda: self.editStyle(tree, explorer))                    
        actions.append(editStyleAction)               
        return actions 
    
    
    def acceptDroppedItem(self, tree, explorer, item): 
        if isinstance(item, (GsStyleItem, QgsStyleItem)):  
            if isinstance(self.parent(), GsLayerItem):
                destinationItem = self.parent()
                addDraggedStyleToLayer(explorer, item, destinationItem)
                return [destinationItem]
            elif isinstance(self.parent(), GsStylesItem) and isinstance(item, QgsStyleItem):
                destinationItem = self.parent()
                publishDraggedStyle(explorer, item.element.name(), destinationItem)
                return [destinationItem]              
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    
    def editStyle(self, tree, explorer):
        dlg = SldEditorDialog(self.element, explorer)
        dlg.exec_()
        
    def deleteStyle(self, tree, explorer):
        self.deleteElements([self], tree, explorer)
        
    def removeStyleFromLayer(self, tree, explorer):
        layer = self.parent().element        
        styles = layer.styles
        styles = [style for style in styles if style.name != self.element.name]            
        layer.styles = styles 
        explorer.run(self.parentCatalog().save, 
                "Remove style '" + self.element.name + "' from layer '" + layer.name, 
                tree.findAllItems(self.parent().element),
                layer)
    
    def setAsDefaultStyle(self, tree, explorer):
        layer = self.parent().element        
        styles = layer.styles
        styles = [style for style in styles if style.name != self.element.name]
        default = layer.default_style
        if default is not None:
            styles.append(default)
        layer.default_style = self.element
        layer.styles = styles 
        explorer.run(self.parentCatalog().save, 
                "Set style '" + self.element.name + "' as default style for layer '" + layer.name + "'", 
                tree.findAllItems(self.parent().element),
                layer)          
    
                      
class GsWorkspaceItem(GsTreeItem): 
    def __init__(self, workspace, isDefault):
        self.catalog = workspace.catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/workspace.png")                 
        self.isDefault = isDefault        
        name = workspace.name if not isDefault else workspace.name + " [default workspace]"
        GsTreeItem.__init__(self, workspace, icon, name)    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)  
        
    def populate(self):
        stores = self.element.catalog.get_stores(self.element)
        for store in stores:
            storeItem = GsStoreItem(store)
            storeItem.populate()
            self.addChild(storeItem)         
                   
    def acceptDroppedItem(self, tree, explorer, item):                        
        if isinstance(item, QgsGroupItem):                
            catalog = self.parentCatalog()
            if catalog is None:
                return
            workspace = self.parentWorkspace()
            if workspace is None:
                workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return explorer.tree.findAllItems(catalog) 
        elif isinstance(item, QgsLayerItem):
            publishDraggedLayer(explorer, item.element, self.element)
            return explorer.tree.findAllItems(self.element.catalog)
        elif isinstance(item, PgTableItem):
            catalog = self.parentCatalog()
            workspace = self.element
            toUpdate = []
            if workspace is not None:
                publishDraggedTable(explorer, item.element, workspace)
                toUpdate.append(explorer.tree.findAllItems(catalog)[0])  
            return toUpdate        
                                    
                                     
    def contextMenuActions(self, tree, explorer):
        setAsDefaultAction = QtGui.QAction("Set as default workspace", explorer)
        setAsDefaultAction.triggered.connect(lambda: self.setAsDefaultWorkspace(explorer))
        setAsDefaultAction.setEnabled(not self.isDefault)                                
        deleteWorkspaceAction = QtGui.QAction("Delete", explorer)
        deleteWorkspaceAction.triggered.connect(lambda: self.deleteWorkspace(tree, explorer))
        return[setAsDefaultAction, deleteWorkspaceAction]
        
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    
    def deleteWorkspace(self, tree, explorer):
        self.deleteElements([self], tree, explorer)
        
    def setAsDefaultWorkspace(self, explorer):
        explorer.run(self.parentCatalog().set_default_workspace, 
                 "Set workspace '" + self.element.name + "' as default workspace",
                 [self.parent()],
                 self.element.name)
        
    def startDropEvent(self):
        self.uris = []        
        
    def acceptDroppedUri(self, explorer, uri):        
        self.uris.append(uri) 
    
    def finishDropEvent(self, explorer):        
        if self.uris:
            catalog = self.parentCatalog()
            files = []
            for uri in self.uris:
                try:
                    files.append(uri.split(":",3)[-1])
                except Exception, e:                    
                    pass            
            workspace = self.element                            
            for i, filename in enumerate(files):
                explorer.progress.setValue(i)
                layerName = QtCore.QFileInfo(filename).completeBaseName()
                layer = QgsVectorLayer(filename, layerName, "ogr")    
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    layer.deleteLater()
                    explorer.setInfo("Error reading file {} or it is not a valid vector layer file".format(filename), 1)                                
                else:
                    publishDraggedLayer(explorer, layer, workspace)
            return [explorer.tree.findAllItems(catalog)[0]]
        else:
            return []        
                                     
class GsStoreItem(GsTreeItem): 
    def __init__(self, store):
        if isinstance(store, DataStore):
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer_polygon.png")
        else:
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/grid.jpg")             
        GsTreeItem.__init__(self, store, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)  

    def populate(self):   
        resources = self.element.get_resources()
        for resource in resources:
            resourceItem = GsResourceItem(resource)                        
            self.addChild(resourceItem)        

    def acceptDroppedItem(self, tree, explorer, item):  
        if isinstance(item, QgsLayerItem):      
            publishDraggedLayer(explorer, item.element, self.element.workspace)
            return explorer.tree.findAllItems(self.element.catalog)        
    
    def contextMenuActions(self, tree, explorer):        
        deleteStoreAction = QtGui.QAction("Delete", explorer)
        deleteStoreAction.triggered.connect(lambda: self.deleteStore(tree, explorer))
        return[deleteStoreAction]
                
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):        
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
                    
    def deleteStore(self, tree, explorer):
        self.deleteElements([self], tree, explorer)
        
class GsResourceItem(GsTreeItem): 
    def __init__(self, resource):  
        if isinstance(resource, Coverage):
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/grid.jpg")
        else:
            icon = None#QtGui.QIcon(os.path.dirname(__file__) + "/../images/workspace.png")
        GsTreeItem.__init__(self, resource, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)  

    def acceptDroppedItem(self, tree, explorer, item):  
        if isinstance(item, QgsLayerItem):      
            publishDraggedLayer(explorer, item.element, self.element.workspace)
            return explorer.tree.findAllItems(self.element.catalog)
    
    def contextMenuActions(self, tree, explorer):
        deleteResourceAction = QtGui.QAction("Delete", explorer)
        deleteResourceAction.triggered.connect(lambda: self.deleteResource(tree, explorer))
        return[deleteResourceAction]
                
    def deleteResource(self, tree, explorer):
        self.deleteElements([self], tree, explorer)      

#### GWC ####

class GwcLayersItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/gwc.png")
        GsTreeItem.__init__(self, None, icon, "GeoWebCache layers")                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)

    def populate(self):
        catalog = self.parentCatalog()
        self.element = Gwc(catalog)        
        layers = self.element.layers()
        for layer in layers:
            item = GwcLayerItem(layer)
            self.addChild(item)

    def acceptDroppedItem(self, tree, explorer, item):  
        if isinstance(item, GsLayerItem):      
            if createGwcLayer(explorer, item.element):
                return [self]
        return []
    
    def contextMenuActions(self, tree, explorer):
        addGwcLayerAction = QtGui.QAction("New GWC layer...", explorer)
        addGwcLayerAction.triggered.connect(lambda: self.addGwcLayer(tree, explorer))
        return [addGwcLayerAction]        
               
     
    def addGwcLayer(self, tree, explorer):
        cat = self.parentCatalog()
        layers = cat.get_layers()              
        dlg = EditGwcLayerDialog(layers, None)
        dlg.exec_()        
        if dlg.gridsets is not None:
            layer = dlg.layer
            gwc = Gwc(layer.catalog)
            
            #TODO: this is a hack that assumes the layer belong to the same workspace
            typename = layer.resource.workspace.name + ":" + layer.name
            
            gwclayer= GwcLayer(gwc, typename, dlg.formats, dlg.gridsets, dlg.metaWidth, dlg.metaHeight)
            catItem = tree.findAllItems(cat)[0]            
            explorer.run(gwc.addLayer,
                              "Create GWC layer '" + layer.name + "'",
                              [catItem.gwcItem],
                              gwclayer)             
                            

          
                
class GwcLayerItem(GsTreeItem): 
    def __init__(self, layer):          
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")        
        GsTreeItem.__init__(self, layer, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)
        
    def contextMenuActions(self, tree, explorer):
        editGwcLayerAction = QtGui.QAction("Edit...", explorer)
        editGwcLayerAction.triggered.connect(lambda: self.editGwcLayer(explorer))           
        seedGwcLayerAction = QtGui.QAction("Seed...", explorer)
        seedGwcLayerAction.triggered.connect(lambda: self.seedGwcLayer(explorer))        
        emptyGwcLayerAction = QtGui.QAction("Empty", explorer)
        emptyGwcLayerAction.triggered.connect(lambda: self.emptyGwcLayer(explorer))                  
        deleteLayerAction = QtGui.QAction("Delete", explorer)
        deleteLayerAction.triggered.connect(lambda: self.deleteLayer(tree, explorer))
        return[editGwcLayerAction, seedGwcLayerAction, emptyGwcLayerAction, deleteLayerAction]

    def acceptDroppedItem(self, tree, explorer, item):  
        if isinstance(item, GsLayerItem):      
            if createGwcLayer(explorer, item.element):
                return [self.parent()]
        return []
        
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        deleteSelectedAction = QtGui.QAction("Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    

    def _getDescriptionHtml(self, tree, explorer):                        
        html = u'<div style="background-color:#ffffcc;"><h1>&nbsp; ' + self.text(0) + ' (GWC layer)</h1></div></br>'  
        html += '<p><b>Seeding status</b></p>'     
        try:
            state = self.element.getSeedingState()
            if state is None:
                html += "<p>No seeding tasks exist for this layer</p>"
            else:
                html += "<p>This layer is being seeded. Processed {} tiles of {}</p>".format(state[0], state[1])
                html += '<p><a href="update">update</a> - <a href="kill">kill</a></p>'
        except SeedingStatusParsingError:
            html += '<p>Cannot determine running seeding tasks for this layer</p>'
        actions = self.contextMenuActions(tree, explorer)
        html += "<p><b>Available actions</b></p><ul>"
        for action in actions:
            if action.isEnabled():
                html += '<li><a href="' + action.text() + '">' + action.text() + '</a></li>\n'
        html += '</ul>'
        return html 
        
    
    def linkClicked(self, tree, explorer, url):
        TreeItem.linkClicked(self,tree, explorer, url)        
        if url.toString() == 'kill':
            try:
                self.element.killSeedingTasks()
            except FailedRequestError:
                #TODO:
                return
        text = self.getDescriptionHtml(tree, explorer)
        self.description.setHtml(text)
        
          
    def deleteLayer(self, tree, explorer):
        self.deleteElements([self], tree, explorer)      
        
        
    def emptyGwcLayer(self, explorer):
        layer = self.element   
        #TODO: confirmation dialog??    
        explorer.run(layer.truncate,
                          "Truncate GWC layer '" + layer.name + "'",
                          [],
                          )            
    def seedGwcLayer(self, explorer):
        layer = self.element   
        dlg = SeedGwcLayerDialog(layer)
        dlg.show()
        dlg.exec_()
        if dlg.format is not None:
            explorer.run(layer.seed,
                              "Request seed for GWC layer '" + layer.name + "' ",
                              [],
                              dlg.operation, dlg.format, dlg.gridset, dlg.minzoom, dlg.maxzoom, dlg.extent)
    
    def editGwcLayer(self, explorer):
        layer = self.element   
        dlg = EditGwcLayerDialog([layer], layer)
        dlg.exec_()
        if dlg.gridsets is not None:
            explorer.run(layer.update,
                              "Update GWC layer '" + layer.name + "'",
                              [],
                              dlg.formats, dlg.gridsets, dlg.metaWidth, dlg.metaHeight)
            
            
########### WPS #####################
            
class GsProcessesItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/process.png")
        GsTreeItem.__init__(self, None, icon, "WPS processes")                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def populate(self):
        self.element = Wps(self.catalog)        
        try:
            processes = self.element.processes()
        except:
            #the WPS extension might not be installed
            processes = []
        for process in processes:
            item = GsProcessItem(process)
            self.addChild(item)
            

class GsProcessItem(GsTreeItem): 
    def __init__(self, process):
        #self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/process.png")
        GsTreeItem.__init__(self, None, icon, process)                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            

################# SETTINGS ###################


class GsSettingsItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/config.png")
        settings = Settings(self.catalog)
        GsTreeItem.__init__(self, settings, icon, "Settings")                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def descriptionWidget(self, tree, explorer):                
        self.description = ParameterEditor(self.element, explorer) 
        return self.description 
            
class GsSettingItem(GsTreeItem): 
    def __init__(self, settings, name, value):
        self.catalog = settings.catalog        
        GsTreeItem.__init__(self, None, None, name) 
        self.setText(1, value)                                   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                         
            
            
###################################################3
                        
def publishDraggedGroup(self, explorer, groupItem, catalog, workspace):        
    groupName = groupItem.element
    groups = qgislayers.getGroups()   
    group = groups[groupName]           
    gslayers= [layer.name for layer in catalog.get_layers()]
    missing = []         
    for layer in group:            
        if layer.name() not in gslayers:
            missing.append(layer)         
    if missing:
        explorer.progress.setMaximum(len(missing))
        progress = 0
        ogcat = OGCatalog(catalog)                  
        for layer in missing:
            explorer.progress.setValue(progress)                                           
            explorer.run(ogcat.publishLayer,
                     "Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1                                                            
        explorer.progress.setValue(progress)  
    names = [layer.name() for layer in group]      
    layergroup = catalog.create_layergroup(groupName, names, names)
    explorer.run(catalog.save, "Create layer group from group '" + groupName + "'", 
             [], layergroup)       

def publishDraggedLayer(explorer, layer, workspace):
    cat = workspace.catalog  
    ogcat = OGCatalog(cat)                                
    explorer.run(ogcat.publishLayer,
             "Publish layer from layer '" + layer.name() + "'",
             [],
             layer, workspace, True)
    
def publishDraggedTable(explorer, table, workspace):    
    cat = workspace.catalog                          
    explorer.run(_publishTable,
             "Publish table from table '" + table.name + "'",
             [],
             table, cat, workspace)
    
            
def _publishTable(table, catalog = None, workspace = None):
    if catalog is None:
        pass       
    workspace = workspace if workspace is not None else catalog.get_default_workspace()
    connection = table.conn   
    geodb = connection.geodb     
    catalog.create_pg_featurestore(connection.name,                                           
                                   workspace = workspace,
                                   overwrite = True,
                                   host = geodb.host,
                                   database = geodb.dbname,
                                   schema = table.schema,
                                   port = geodb.port,
                                   user = geodb.user,
                                   passwd = geodb.passwd)
    catalog.create_pg_featuretype(table.name, connection.name, workspace, "EPSG:" + str(table.srid))  

def publishDraggedStyle(explorer, layerName, catalogItem):
    ogcat = OGCatalog(catalogItem.element)
    toUpdate = []
    for idx in range(catalogItem.childCount()):
        subitem = catalogItem.child(idx)
        if isinstance(subitem, GsStylesItem):
            toUpdate.append(subitem)
            break                
    explorer.run(ogcat.publishStyle,
             "Publish style from layer '" + layerName + "'",
             toUpdate,
             layerName, True, layerName)

def addDraggedLayerToGroup(explorer, layer, groupItem):    
    group = groupItem.element
    styles = group.styles
    layers = group.layers
    if layer.name not in layers:
        layers.append(layer.name)
        styles.append(layer.default_style.name)
    group.dirty.update(layers = layers, styles = styles)
    explorer.run(layer.catalog.save,
                 "Update group '" + group.name + "'",
                 [groupItem],
                 group)
    
def addDraggedStyleToLayer(explorer, styleItem, layerItem):
    catalog = layerItem.element.catalog  
    if isinstance(styleItem, QgsStyleItem):
        styleName = styleItem.element.name()                   
        catalogItem = explorer.tree.findAllItems(catalog)[0]
        publishDraggedStyle(explorer, styleName, catalogItem)     
        style = catalog.get_style(styleName)
    else:         
        style = styleItem.element            
    layer = layerItem.element
    styles = layer.styles                            
    styles.append(style)
    layer.styles = styles                        
    explorer.run(catalog.save, 
             "Add style '" + style.name + "' to layer '" + layer.name + "'",
             [layerItem],
             layer)  
         
        
def createGwcLayer(explorer, layer):                
    dlg = EditGwcLayerDialog([layer], None)
    dlg.exec_()        
    if dlg.gridsets is not None:
        gwc = Gwc(layer.catalog)
        
        #TODO: this is a hack that assumes the layer belong to the same workspace
        typename = layer.resource.workspace.name + ":" + layer.name
        
        gwclayer= GwcLayer(gwc, typename, dlg.formats, dlg.gridsets, dlg.metaWidth, dlg.metaHeight)
        explorer.run(gwc.addLayer,
                          "Create GWC layer '" + layer.name + "'",
                          [],
                          gwclayer)  
        return True
    else:
        return False                 
