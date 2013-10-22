import os
from qgis.core import *
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from opengeo.qgis import layers as qgislayers
from opengeo.geoserver.store import DataStore, CoverageStore
from opengeo.geoserver.resource import Coverage, FeatureType
from dialogs.catalogdialog import DefineCatalogDialog
from opengeo.geoserver.style import Style
from opengeo.geoserver.layer import Layer
from dialogs.styledialog import AddStyleToLayerDialog, StyleFromLayerDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.exploreritems import TreeItem
from dialogs.groupdialog import LayerGroupDialog
from dialogs.workspacedialog import DefineWorkspaceDialog
from opengeo.geoserver.layergroup import UnsavedLayerGroup
from opengeo.gui.qgsexploreritems import QgsLayerItem, QgsGroupItem,\
    QgsStyleItem
from opengeo.geoserver.catalog import Catalog
from opengeo.gui.pgexploreritems import PgTableItem
import traceback
from opengeo.geoserver.wps import Wps
from dialogs.crsdialog import CrsSelectionDialog
from opengeo.geoserver.settings import Settings
from opengeo.gui.parametereditor import ParameterEditor
from dialogs.sldeditor import SldEditorDialog
from opengeo.gui.gwcexploreritems import GwcLayersItem
from opengeo import config
from opengeo.qgis.utils import tempFilename
from opengeo.qgis.sldadapter import adaptGsToQgs, getGeomTypeFromSld,\
    getGsCompatibleSld
from opengeo.geoserver.util import getLayerFromStyle
from opengeo.geoserver.geonode import Geonode

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
        uniqueStyles = []
        workspacesToUpdate = []
        for item in selected:
            elements.append(item.element)
            if isinstance(item, GsStoreItem):
                for idx in range(item.childCount()):
                    subitem = item.child(idx)
                    elements.insert(0, subitem.element)
            elif isinstance(item, GsLayerItem):
                uniqueStyles.extend(self.uniqueStyles(item.element)) 
                workspace = item.element.resource.workspace
                workspacesToUpdate.extend(tree.findAllItems(workspace))                                              
        toUpdate = set(item.parent() for item in selected)                
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
        
        settings = QSettings()
        deleteStyle = bool(settings.value("/OpenGeo/Settings/GeoServer/DeleteStyle", True, bool))
        recurse = bool(settings.value("/OpenGeo/Settings/GeoServer/Recurse", True, bool)) 

        elements[0:0] = dependent 
        if recurse:
            toUpdate.update(workspacesToUpdate)            
        if deleteStyle:
            elements.extend(uniqueStyles)  
            stylesEntriesToUpdate = set() 
            for e in uniqueStyles:                
                items = tree.findAllItems(e);
                for item in items:
                    #the item representing the layer we are deleting will be here, but we have to ignore it
                    #and update only the "styles" item
                    if isinstance(item.parent(), GsStylesItem):
                        stylesEntriesToUpdate.add(item.parent())
                        break                       
            toUpdate.update(stylesEntriesToUpdate)         
        explorer.setProgressMaximum(len(elements), "Deleting elements")   
        for progress, element in enumerate(elements):
            explorer.setProgress(progress)    
            #we run this delete operation this way, to ignore the error in case we are trying to delete
            #something that doesn't exist which might happen if a previous deletion has purged the element
            #we now want to delete. It is deleted already anyway, so we should not raise any exception
            try:
                element.catalog.delete(element, recurse = recurse, purge = True)
            except:
                pass                
        explorer.setProgress(len(elements))
        for item in toUpdate:
            if item is not None:
                item.refreshContent(explorer)
        if None in toUpdate:
            explorer.refreshContent()
        explorer.resetActivity()
        explorer.setDescriptionWidget()
    
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
                    if group.layers is None:
                        continue                   
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
    
    def iconPath(self):
        return os.path.dirname(__file__) + "/../images/geoserver.png"
                                     
    
class GsCatalogsItem(GsTreeItem):    
    def __init__(self): 
        self._catalogs = {}
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")        
        GsTreeItem.__init__(self, None, icon, "GeoServer catalogs") 
        settings = QSettings()
        saveCatalogs = bool(settings.value("/OpenGeo/Settings/GeoServer/SaveCatalogs", False, bool))  
        if saveCatalogs:
            settings.beginGroup("/OpenGeo/GeoServer")
            for name in settings.childGroups():
                settings.beginGroup(name)
                url = unicode(settings.value("url"))                
                password = unicode(settings.value("password"))
                username = unicode(settings.value("username"))
                geonodeUrl = unicode(settings.value("geonode"))
                geonode = Geonode(geonodeUrl)                
                cat = Catalog(url, username, password)
                geoserverItem = GsCatalogItem(cat, name, geonode)                
                self.addChild(geoserverItem)
                settings.endGroup()
            settings.endGroup()
           

    def contextMenuActions(self, tree, explorer):  
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")      
        createCatalogAction = QtGui.QAction(icon, "New catalog...", explorer)
        createCatalogAction.triggered.connect(lambda: self.addGeoServerCatalog(explorer))
        return [createCatalogAction]
                    
    def addGeoServerCatalog(self, explorer):         
        dlg = DefineCatalogDialog()
        dlg.exec_()                        
        if dlg.ok:            
            try:
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
                cat = Catalog(dlg.url, dlg.username, dlg.password)               
                v = cat.gsversion()
                supported = v.startswith("2.3") or v.startswith("2.4")
                if not supported:
                    ret = QtGui.QMessageBox.warning(explorer, "GeoServer catalog definition",
                                    "The specified catalog seems to be running an older version of GeoServer\n"
                                    "That might cause unexpected behaviour.\nDo you want to add the catalog anyway?",
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,                                
                                    QtGui.QMessageBox.No);
                    if ret == QtGui.QMessageBox.No:
                        return
                    
                name = dlg.name
                i = 2
                while name in self._catalogs.keys():
                    name = dlg.name + "_" + str(i)
                    i += 1
                geonode = Geonode(dlg.geonodeUrl)
                geoserverItem = GsCatalogItem(cat, name, geonode)
                geoserverItem.populate()                
                if geoserverItem is not None:
                    self._catalogs[name] = cat
                    self.addChild(geoserverItem)
                    self.setExpanded(True)            
            except:                
                explorer.setInfo("Could not connect to catalog:\n" + traceback.format_exc(), 1)
                return
            finally:
                QtGui.QApplication.restoreOverrideCursor()
                
                                      
            
class GsLayersItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        GsTreeItem.__init__(self, None, icon, "GeoServer Layers")
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
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate  
        elif isinstance(item, QgsGroupItem):                
            catalog = self.parentCatalog()
            if catalog is None:
                return
            workspace = self.parentWorkspace()
            if workspace is None:
                workspace = self.getDefaultWorkspace()
            publishDraggedGroup(explorer, item, catalog, workspace)
            return tree.findAllItems(catalog)
        elif isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate  
        else:
            return []
        
    def acceptDroppedUris(self, tree, explorer, uris):  
        return addDraggedUrisToWorkspace(uris, self.parentCatalog(), self.getDefaultWorkspace(), explorer, tree)           
                        
class GsGroupsItem(GsTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        GsTreeItem.__init__(self, None, icon, "GeoServer Groups")           
        
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
            return tree.findAllItems(catalog)     
        else:
            return []  
    
    def contextMenuActions(self, tree, explorer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")           
        createGroupAction = QtGui.QAction(icon, "New group...", explorer)
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
        GsTreeItem.__init__(self, None, icon, "GeoServer Workspaces")  
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
            return tree.findAllItems(catalog)
        elif isinstance(item, QgsLayerItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedLayer(explorer, item.element, workspace)
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate   
        elif isinstance(item, PgTableItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                publishDraggedTable(explorer, item.element, workspace)
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate   
        else:
            return []        
        
    def acceptDroppedUris(self, tree, explorer, uris):                        
        return addDraggedUrisToWorkspace(uris, self.parentCatalog(), self.getDefaultWorkspace(), explorer, tree)
                            
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")        
        createWorkspaceAction = QtGui.QAction(icon, "New workspace...", explorer)
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
        GsTreeItem.__init__(self, None, icon, "GeoServer Styles")
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled) 
                    
    def populate(self):
        styles = self.parentCatalog().get_styles()
        for style in styles:
            styleItem = GsStyleItem(style, False)                
            self.addChild(styleItem)

    def acceptDroppedItem(self, tree, explorer, item):
        if isinstance(item, QgsStyleItem):
            catalog = self.parentCatalog()
            workspace = self.getDefaultWorkspace()
            toUpdate = []
            if workspace is not None:
                catalogItem = tree.findAllItems(catalog)[0]
                publishDraggedStyle(explorer, item.element.name(), catalogItem)
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate  
        else:
            return []
        
    def contextMenuActions(self, tree, explorer):   
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")     
        createStyleFromLayerAction = QtGui.QAction(icon, "New style from QGIS layer...", explorer)
        createStyleFromLayerAction.triggered.connect(lambda: self.createStyleFromLayer(explorer))
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/clean.png")      
        cleanAction = QtGui.QAction(icon, "Clean (remove unused styles)", explorer)
        cleanAction.triggered.connect(lambda: self.cleanStyles(explorer))
        consolidateStylesAction = QtGui.QAction(icon, "Consolidate styles", explorer)
        consolidateStylesAction.triggered.connect(lambda: self.consolidateStyles(tree, explorer))
        return [createStyleFromLayerAction, cleanAction, consolidateStylesAction] 
           
    def consolidateStyles(self, tree, explorer):
        catalog = self.parentCatalog()
        catalogItem = tree.findAllItems(catalog)[0]
        ogcat = OGCatalog(self.catalog)
        explorer.run(ogcat.consolidateStyles, "Consolidate styles", [self, catalogItem.layersItem])
        
    def cleanStyles(self, explorer):
        ogcat = OGCatalog(self.catalog)
        explorer.run(ogcat.cleanUnusedStyles, "Clean (remove unused styles)", [self])
    
    def createStyleFromLayer(self, explorer):  
        dlg = StyleFromLayerDialog()
        dlg.exec_()      
        if dlg.layer is not None:
            ogcat = OGCatalog(self.catalog)        
            explorer.run(ogcat.publishStyle, 
                     "Create style from layer '" + dlg.layer + "'",
                     [self],
                     dlg.layer, True, dlg.name)


class GsCatalogItem(GsTreeItem): 
    def __init__(self, catalog, name, geonode): 
        self.catalog = catalog
        self.geonode = geonode
        self.isConnected = False
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver_gray.png")
        GsTreeItem.__init__(self, catalog, icon, name) 
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled) 
                
    def populate(self):
        self.isConnected = False        
        self.workspacesItem = GsWorkspacesItem(self.catalog)                                      
        self.workspacesItem.populate()
        self.addChild(self.workspacesItem)
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
        self.geonodesItem = GsGeonodesItem(self.geonode)                        
        self.addChild(self.geonodesItem)   
        self.wpsItem = GsProcessesItem(self.catalog)                        
        self.addChild(self.wpsItem)
        self.wpsItem.populate()
        self.settingsItem = GsSettingsItem(self.catalog)                        
        self.addChild(self.settingsItem)             
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
        self.setIcon(0, icon) 
        self.isConnected = True                    

    def acceptDroppedItem(self, tree, explorer, item):
        if not self.isConnected:
            return []
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
        elif isinstance(item, PgTableItem):
            catalog = self.element
            workspace = self.getDefaultWorkspace()                
            publishDraggedTable(explorer, item.element, workspace)            
            return [self]  
        else:
            return []       
        
    def contextMenuActions(self, tree, explorer):          
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")      
        removeCatalogAction = QtGui.QAction(icon, "Remove", explorer)
        removeCatalogAction.triggered.connect(lambda: self.removeCatalog(explorer))
        actions = [removeCatalogAction]            
        if self.isConnected:
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/clean.png")      
            cleanAction = QtGui.QAction(icon, "Clean (remove unused elements)", explorer)
            cleanAction.triggered.connect(lambda: self.cleanCatalog(explorer))
            actions.append(cleanAction)
        
        return actions 
        
    def cleanCatalog(self, explorer):
        ogcat = OGCatalog(self.catalog)        
        explorer.run(ogcat.clean, "Clean (remove unused element)", [self.workspacesItem, self.stylesItem])
        
    def removeCatalog(self, explorer):
        name = self.text(0)
        if name in explorer.catalogs():
            del explorer.catalogs()[name]
        settings = QSettings()
        settings.beginGroup("/OpenGeo/GeoServer/" + name) 
        settings.remove(""); 
        settings.endGroup();            
        self.parent().takeChild(self.parent().indexOfChild(self))  
        explorer.setDescriptionWidget(QtGui.QWidget())
        explorer.setToolbarActions([])
         
        
    def _getDescriptionHtml(self, tree, explorer):                        
        if self.isConnected:            
            return self.catalog.about()
        else:
            html = ('<p>You are not connected to this catalog.' 
                    '<a href="refresh">Refresh</a> to connect to it and populate the catalog item</p>')     
            return html 
            
    def linkClicked(self, tree, explorer, url):
        if not self.isConnected:            
            explorer.run(self.populate, "Populate GeoServer item", []) 
            explorer.catalogs()[self.text(0)] = self.catalog         
    
    def acceptDroppedUris(self, tree, explorer, uris): 
        if not self.isConnected:
            return []
        return addDraggedUrisToWorkspace(uris, self.element, self.getDefaultWorkspace(), explorer, tree)                    
           
                                
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
            addDraggedStyleToLayer(tree, explorer, item, self)
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
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate  
        else:
            return []
    
    def _getDescriptionHtml(self, tree, explorer):  
        html = '<p><h3><b>Properties</b></h3></p><ul>'
        html += '<li><b>Name: </b>' + str(self.element.name) + '</li>\n'
        html += '<li><b>Title: </b>' + str(self.element.resource.title) + ' &nbsp;<a href="modify:title">Modify</a></li>\n'     
        html += '<li><b>Abstract: </b>' + str(self.element.resource.abstract) + ' &nbsp;<a href="modify:abstract">Modify</a></li>\n'
        html += ('<li><b>SRS: </b>' + str(self.element.resource.projection) + ' &nbsp;<a href="modify:srs">Modify</a></li>\n')        
        bbox = self.element.resource.latlon_bbox
        if bbox is not None:                    
            html += '<li><b>Bounding box (lat/lon): </b></li>\n<ul>'
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
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
            removeLayerFromGroupAction = QtGui.QAction(icon, "Remove layer from group", explorer)            
            removeLayerFromGroupAction.setEnabled(count > 1)
            removeLayerFromGroupAction.triggered.connect(lambda: self.removeLayerFromGroup(explorer))
            actions.append(removeLayerFromGroupAction)      
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/up.png")                                          
            moveLayerUpInGroupAction = QtGui.QAction(icon, "Move up", explorer)            
            moveLayerUpInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerUpInGroupAction.triggered.connect(lambda: self.moveLayerUpInGroup(explorer))
            actions.append(moveLayerUpInGroupAction)
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/down.png")
            moveLayerDownInGroupAction = QtGui.QAction(icon, "Move down", explorer)            
            moveLayerDownInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerDownInGroupAction.triggered.connect(lambda: self.moveLayerDownInGroup(explorer))
            actions.append(moveLayerDownInGroupAction)
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/top.png")
            moveLayerToFrontInGroupAction = QtGui.QAction(icon, "Move to front", explorer)            
            moveLayerToFrontInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerToFrontInGroupAction.triggered.connect(lambda: self.moveLayerToFrontInGroup(explorer))
            actions.append(moveLayerToFrontInGroupAction)
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/bottom.png")
            moveLayerToBackInGroupAction = QtGui.QAction(icon, "Move to back", explorer)            
            moveLayerToBackInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerToBackInGroupAction.triggered.connect(lambda: self.moveLayerToBackInGroup(explorer))
            actions.append(moveLayerToBackInGroupAction)
        else:
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
            addStyleToLayerAction = QtGui.QAction(icon, "Add style to layer...", explorer)
            addStyleToLayerAction.triggered.connect(lambda: self.addStyleToLayer(explorer))                    
            actions.append(addStyleToLayerAction)   
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
            deleteLayerAction = QtGui.QAction(icon, "Delete", None)
            deleteLayerAction.triggered.connect(lambda: self.deleteLayer(tree, explorer))
            actions.append(deleteLayerAction)         
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/import_into_qgis.png")                       
            addLayerAction = QtGui.QAction(icon, "Add to current QGIS project", explorer)
            addLayerAction.triggered.connect(lambda: self.addLayerToProject(explorer))
            actions.append(addLayerAction) 
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geonode.png")                       
            publishToGeonodeAction = QtGui.QAction(icon, "Publish to GeoNode", explorer)
            publishToGeonodeAction.triggered.connect(lambda: self.publishToGeonode(tree, explorer))
            actions.append(publishToGeonodeAction)  
            
        return actions
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")       
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        createGroupAction = QtGui.QAction(icon, "Create group...", explorer)
        createGroupAction.triggered.connect(lambda: self.createGroupFromLayers(selected, tree, explorer))        
        return [deleteSelectedAction, createGroupAction]
                 
            
    def publishToGeonode(self, tree, explorer):
        #There must be a better way to access the geonode instance from here or maybe require a new method
        geonode = self.parent().parent().geonode
        layer = self.element.name
        #TODO parse JSON output from publishGeoServer and display a feedback message to the user
        explorer.run(geonode.publishGeoserverLayer,
                     "Publishing '" + layer + "' to GeoNode",
                     [],
                     layer)
    
    def createGroupFromLayers(self, selected, tree, explorer):        
        name, ok = QtGui.QInputDialog.getText(None, "Group name", "Enter the name of the group to create")        
        if not ok:
            return
        catalog = self.element.catalog
        catalogItem = tree.findAllItems(catalog)[0]
        if catalogItem is not None:
            groupsItem = catalogItem.groupsItem
        else:
            groupsItem = None
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
        #TODO: fix this
        cat = OGCatalog(self.parentCatalog()) 
        try:
            cat.addLayerToProject(self.element.name)
            explorer.setInfo("Layer '" + self.element.name + "' correctly added to QGIS project")
            explorer.updateQgisContent()
        except Exception, e:
            explorer.setInfo(str(e), 1)  
                                

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
            if layer is not None:
                if ':' in layer:
                    layer = layer.split(':')[1]
                layerItem = GsLayerItem(layersDict[layer])                          
                self.addChild(layerItem)
            
            
    def acceptDroppedItem(self, tree, explorer, item):                        
        if isinstance(item, GsLayerItem):
            addDraggedLayerToGroup(explorer, item.element, self)
            return [self] 
        else:
            return []           
            
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit.png")
        editLayerGroupAction = QtGui.QAction(icon, "Edit...", explorer)
        editLayerGroupAction.triggered.connect(lambda: self.editLayerGroup(explorer))  
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")           
        deleteLayerGroupAction = QtGui.QAction(icon, "Delete", explorer)
        deleteLayerGroupAction.triggered.connect(lambda: self.deleteLayerGroup(tree, explorer))
        return [editLayerGroupAction, deleteLayerGroupAction]
       
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")        
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
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
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | 
                      QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)        
        
    def contextMenuActions(self, tree, explorer):   
        actions = []
        if isinstance(self.parent(), GsLayerItem):
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/default-style.png")
            setAsDefaultStyleAction = QtGui.QAction(icon, "Set as default style", explorer)
            setAsDefaultStyleAction.triggered.connect(lambda: self.setAsDefaultStyle(tree, explorer))
            setAsDefaultStyleAction.setEnabled(not self.isDefault)
            actions.append(setAsDefaultStyleAction)  
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
            removeStyleFromLayerAction = QtGui.QAction(icon, "Remove style from layer", explorer)
            removeStyleFromLayerAction.triggered.connect(lambda: self.removeStyleFromLayer(tree, explorer))
            removeStyleFromLayerAction.setEnabled(not self.isDefault)                        
            actions.append(removeStyleFromLayerAction)                           
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit.png")
            editStyleAction = QtGui.QAction(icon, "Edit...", explorer)
            editStyleAction.triggered.connect(lambda: self.editStyle(tree, explorer, self.parent().element))
            actions.append(editStyleAction)
        else:                      
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
            deleteStyleAction = QtGui.QAction(icon, "Delete", explorer)
            deleteStyleAction.triggered.connect(lambda: self.deleteStyle(tree, explorer))
            actions.append(deleteStyleAction)
            icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit.png")
            editStyleAction = QtGui.QAction(icon, "Edit...", explorer)
            editStyleAction.triggered.connect(lambda: self.editStyle(tree, explorer))
            actions.append(editStyleAction) 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit_sld.png")
        editSLDAction = QtGui.QAction(icon, "Edit SLD...", explorer)
        editSLDAction.triggered.connect(lambda: self.editSLD(tree, explorer))                    
        actions.append(editSLDAction)               
        return actions 
    
    
    def acceptDroppedItem(self, tree, explorer, item):         
        if isinstance(item, (GsStyleItem, QgsStyleItem)):  
            if isinstance(self.parent(), GsLayerItem):
                destinationItem = self.parent()
                addDraggedStyleToLayer(tree, explorer, item, destinationItem)
                return [destinationItem]
            elif isinstance(self.parent(), GsStylesItem) and isinstance(item, QgsStyleItem):
                catalog = self.parentCatalog()
                catalogItem = tree.findAllItems(catalog)[0]                
                publishDraggedStyle(explorer, item.element.name(), catalogItem)
                return [catalogItem] 
            else:
                return [] 
        else:
            return []            
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    
    def editStyle(self, tree, explorer, gslayer = None): 
        if gslayer is None:
            gslayer = getLayerFromStyle(self.element)               
        if gslayer is not None:
            if not hasattr(gslayer.resource, "attributes"):
                QtGui.QMessageBox.warning(explorer, "Edit style", "Editing raster layer styles is currently not supported")
                return
        sld = self.element.sld_body            
        sld = adaptGsToQgs(sld)              
        sldfile = tempFilename("sld") 
        with open(sldfile, 'w') as f:
            f.write(sld)
        geomtype = getGeomTypeFromSld(sld)        
        uri = geomtype                                          
        if gslayer is not None:
            fields = gslayer.resource.attributes
            fieldsdesc = ['field=%s:double' % f for f in fields if "geom" not in f]
            fieldsstring = '&'.join(fieldsdesc)
            uri += "?" + fieldsstring                                                        
        layer = QgsVectorLayer(uri, "tmp", "memory")                        
        layer.loadSldStyle(sldfile)
        oldSld = getGsCompatibleSld(layer)            
        config.iface.showLayerProperties(layer)
        newSld = getGsCompatibleSld(layer)
        if newSld != oldSld:
            explorer.run(self.element.update_body, "Update style", [], newSld)                 
    
    def editSLD(self, tree, explorer):        
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
            return tree.findAllItems(catalog) 
        elif isinstance(item, QgsLayerItem):
            publishDraggedLayer(explorer, item.element, self.element)
            return tree.findAllItems(self.element.catalog)
        elif isinstance(item, PgTableItem):
            catalog = self.parentCatalog()
            workspace = self.element
            toUpdate = []
            if workspace is not None:
                publishDraggedTable(explorer, item.element, workspace)
                toUpdate.append(tree.findAllItems(catalog)[0])  
            return toUpdate  
        else:
            return []      
                                    
                                     
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/default-workspace.png")
        setAsDefaultAction = QtGui.QAction(icon, "Set as default workspace", explorer)
        setAsDefaultAction.triggered.connect(lambda: self.setAsDefaultWorkspace(explorer))
        setAsDefaultAction.setEnabled(not self.isDefault)    
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")                            
        deleteWorkspaceAction = QtGui.QAction(icon, "Delete", explorer)
        deleteWorkspaceAction.triggered.connect(lambda: self.deleteWorkspace(tree, explorer))
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/clean.png")      
        cleanAction = QtGui.QAction(icon, "Clean (remove unused resources)", explorer)
        cleanAction.triggered.connect(lambda: self.cleanWorkspace(explorer))
        return[setAsDefaultAction, deleteWorkspaceAction, cleanAction]
        
    def cleanWorkspace(self, explorer):
        ogcat = OGCatalog(self.catalog)
        explorer.run(ogcat.cleanUnusedResources, "Clean (remove unused resources)", [self])
    
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteElements(selected, tree, explorer))
        return [deleteSelectedAction]
    
    def deleteWorkspace(self, tree, explorer):
        self.deleteElements([self], tree, explorer)
        
    def setAsDefaultWorkspace(self, explorer):
        explorer.run(self.parentCatalog().set_default_workspace, 
                 "Set workspace '" + self.element.name + "' as default workspace",
                 [self.parent()],
                 self.element.name)
        
    def acceptDroppedUris(self, tree, explorer, uris):            
        return addDraggedUrisToWorkspace(uris, self.parentCatalog(), self.element, explorer, tree)      
                                     
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
            return tree.findAllItems(self.element.catalog)  
        else:
            return []      
    
    def contextMenuActions(self, tree, explorer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")       
        deleteStoreAction = QtGui.QAction(icon, "Delete", explorer)
        deleteStoreAction.triggered.connect(lambda: self.deleteStore(tree, explorer))
        return[deleteStoreAction]
                
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):   
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")     
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
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
            return tree.findAllItems(self.element.catalog)
        else:
            return []
    
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
        deleteResourceAction = QtGui.QAction(icon, "Delete", explorer)
        deleteResourceAction.triggered.connect(lambda: self.deleteResource(tree, explorer))
        return[deleteResourceAction]
                
    def deleteResource(self, tree, explorer):
        self.deleteElements([self], tree, explorer)      


            
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
        GsTreeItem.__init__(self, settings, icon, "GeoServer Settings")                                    
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
                         
    
################# GEONODE ###################


class GsGeonodesItem(GsTreeItem): 
    def __init__(self, geonode):
        self.geonode = geonode
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geonode.png")
        GsTreeItem.__init__(self, None, icon, "GeoNode")                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def _getDescriptionHtml(self, tree, explorer):
        description = '<p> GeoNode URL: ' + self.geonode.url + '</p><p>Right click on a GeoServer layer to publish a layer to GeoNode'
        return description

class GsGeonodeItem(GsTreeItem): 
    def __init__(self):
        #self.catalog = settings.catalog        
        GsTreeItem.__init__(self, None, None, name) 
        self.setText(1, value)                                   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                         
            
            
###################################################
                        
def publishDraggedGroup(explorer, groupItem, catalog, workspace):        
    groupName = groupItem.element
    groups = qgislayers.getGroups()   
    group = groups[groupName]           
    gslayers= [layer.name for layer in catalog.get_layers()]
    missing = []         
    for layer in group:            
        if layer.name() not in gslayers:
            missing.append(layer)         
    if missing:
        explorer.setProgressMaximum(len(missing), "Publish layers")
        progress = 0
        ogcat = OGCatalog(catalog)                  
        for layer in missing:
            explorer.setProgress(progress)                                           
            explorer.run(ogcat.publishLayer,
                     None,#"Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1                                                            
            explorer.setProgress(progress)
        explorer.resetActivity()
    names = [layer.name() for layer in group]      
    layergroup = catalog.create_layergroup(groupName, names, names)
    explorer.run(catalog.save, "Create layer group from group '" + groupName + "'", 
             [], layergroup)       

def publishDraggedLayer(explorer, layer, workspace):
    cat = workspace.catalog  
    ogcat = OGCatalog(cat)                                
    ret = explorer.run(ogcat.publishLayer,
             "Publish layer from layer '" + layer.name() + "'",
             [],
             layer, workspace, True)    
    return ret
    
def publishDraggedTable(explorer, table, workspace):    
    cat = workspace.catalog                          
    return explorer.run(_publishTable,
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
    toUpdate = [catalogItem.stylesItem]                    
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
    
def addDraggedStyleToLayer(tree, explorer, styleItem, layerItem):
    catalog = layerItem.element.catalog  
    if isinstance(styleItem, QgsStyleItem):
        styleName = styleItem.element.name()                   
        catalogItem = tree.findAllItems(catalog)[0]
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

def addDraggedUrisToWorkspace(uris, catalog, workspace, explorer, tree):
    if uris:      
        if len(uris) > 1:  
            explorer.setProgressMaximum(len(uris))                                     
        for i, uri in enumerate(uris):  
            if isinstance(uri, basestring):            
                layerName = QtCore.QFileInfo(uri).completeBaseName()
                layer = QgsRasterLayer(uri, layerName)
            else:                                               
                layer = QgsRasterLayer(uri.uri, uri.name)            
            if not layer.isValid() or layer.type() != QgsMapLayer.RasterLayer:                                                  
                if isinstance(uri, basestring):                                    
                    layerName = QtCore.QFileInfo(uri).completeBaseName()
                    layer = QgsVectorLayer(uri, layerName, "ogr")
                else:                                                           
                    layer = QgsVectorLayer(uri.uri, uri.name, uri.providerKey)                
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    layer.deleteLater()
                    name = uri if isinstance(uri, basestring) else uri.uri 
                    explorer.setInfo("Error reading file {} or it is not a valid layer file".format(name), 1)   
                else:
                    if not publishDraggedLayer(explorer, layer, workspace):                        
                        return []                    
            else:
                if not publishDraggedLayer(explorer, layer, workspace):                    
                    return []
            explorer.setProgress(i + 1)        
        explorer.resetActivity()                
        return [tree.findAllItems(catalog)[0]]
    else:
        return []  
