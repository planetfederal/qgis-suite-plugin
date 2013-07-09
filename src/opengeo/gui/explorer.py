import sys
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from opengeo.qgis import catalog
from opengeo.qgis import layers as qgislayers
from opengeo.core.workspace import Workspace
from opengeo.core.layer import Layer
from opengeo.qgis.catalog import OGCatalog
from opengeo.core.store import CoverageStore, DataStore
from opengeo.core.support import ResourceInfo
from opengeo.core.style import Style
from opengeo.gui.catalogdialog import DefineCatalogDialog
from opengeo.geoserver.catalog import Catalog
import os
from opengeo.core.layergroup import LayerGroup
from opengeo.core import util


class GeoServerExplorer(QtGui.QDialog):
    
    gsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
    layerIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
    groupIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
    styleIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
    
    def __init__(self, parent = None):
        super(GeoServerExplorer, self).__init__()        
        self.catalogs = []
        self.initGui()
        
    def initGui(self):      
        self.resize(400, 600) 
        self.setWindowTitle('GeoServer explorer')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)         
        self.toolbar = QtGui.QToolBar()
        self.addButton = QtGui.QToolButton()
        #self.addButton.setText('Edit')
        self.addAction = QtGui.QAction('Simple', self, triggered=self.addGeoServerCatalog)
        self.addButton.setDefaultAction(self.addAction)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
        self.addButton.setIcon(icon)
        self.toolbar.addWidget(self.addButton)  
        self.verticalLayout.addWidget(self.toolbar)                         
        self.tree = QtGui.QTreeWidget()         
        self.tree.itemClicked.connect(self.treeItemClicked)        
        self.tree.setColumnCount(1)            
        self.tree.header().hide()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showTreePopupMenu)
        self.fillTree()                                                                                  
        self.verticalLayout.addWidget(self.tree) 
        self.setLayout(self.verticalLayout)
        

    
    def treeItemClicked(self, item, column):
        #=======================================================================
        # depth = self.depth(item)
        # if depth == 1:
        #    element = item.data(0, QtCore.Qt.UserRole).toPyObject() 
        #    if isinstance(element, Logentry):#commit 
        #        diffset = element.diffset
        #        self.currentRef = element.commit.ref
        #    else: #working tree
        #        diffset = element
        #        self.currentRef = geogit.WORK_HEAD
        #    self.table.clear()
        #    self.table.setRowCount(len(diffset))
        #    self.table.setHorizontalHeaderLabels(["Path", "Status"])
        #    self.table.horizontalHeader().setMinimumSectionSize(150)            
        #    for i, diff in enumerate(diffset):
        #        self.table.setItem(i, 0, QtGui. QTableWidgetItem(diff.path));
        #        self.table.setItem(i, 1, QtGui. QTableWidgetItem(diff.type()));                
        #    self.table.horizontalHeader().setStretchLastSection(True) 
        #    self.table.resizeRowsToContents()   
        #            
        #=======================================================================
        pass
    
    def addGeoServerCatalog(self):         
        dlg = DefineCatalogDialog()
        dlg.exec_()
        cat = dlg.getCatalog()
        if cat is not None:             
            self.catalogs.append(cat)
            item = self.getGeoServerCatalogItem(cat, dlg.getName())
            catalogsItem = self.tree.topLevelItem(0)
            catalogsItem.addChild(item)
        
    def fillTree(self):
        self.addGeoServerCatalogsToTree()
        self.addQGisProjectToTree()
        
    def addGeoServerCatalogsToTree(self):
        catalogsItem = QtGui.QTreeWidgetItem()
        catalogsItem.setText(0, "GeoServer catalogs")
        catalogsItem.setIcon(0, self.gsIcon)
        for cat in self.catalogs:
            item = self.getGeoServerCatalogItem(cat)            
            catalogsItem.addChild(item)
        self.tree.addTopLevelItem(catalogsItem)
            
    def getGeoServerCatalogItem(self, cat, name):    
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
        try:    
            geoserverItem = CatalogItem(cat, name)
            workspacesItem = WorkspacesItem()            
            workspaces = cat.get_workspaces()
            for workspace in workspaces:
                workspaceItem = WorkspaceItem(workspace, self)
                workspacesItem.addChild(workspaceItem)
                stores = cat.get_stores(workspace)
                for store in stores:
                    storeItem = StoreItem(store)
                    workspaceItem.addChild(storeItem)
                    resources = cat.get_resources(store, workspace)
                    for resource in resources:
                        resourceItem = ResourceItem(resource)                        
                        storeItem.addChild(resourceItem)
            geoserverItem.addChild(workspacesItem)  
            layersItem = LayersItem()            
            layers = cat.get_layers()
            layersDict = {layer.name : layer for layer in layers}
            for layer in layers:
                layerItem = LayerItem(layer)                
                layersItem.addChild(layerItem)
                for style in layer.styles:
                    styleItem = StyleItem(style, False)
                    layerItem.addChild(styleItem)
                if layer.default_style is not None:
                    styleItem = StyleItem(layer.default_style, True)                    
                    layerItem.addChild(styleItem)                
            geoserverItem.addChild(layersItem)
            groupsItem = GroupsItem()
            groups = cat.get_layergroups()
            for group in groups:
                groupItem = GroupItem(group)                
                for layer in group.layers:
                    layerItem = LayerItem(layersDict[layer])                    
                    groupItem.addChild(layerItem)
                groupsItem.addChild(groupItem)            
            geoserverItem.addChild(groupsItem)
            stylesItem = StylesItem()            
            styles = cat.get_styles()
            for style in styles:
                styleItem = StyleItem(style, False)                
                stylesItem.addChild(styleItem)
            geoserverItem.addChild(stylesItem)
            QtGui.QApplication.restoreOverrideCursor()
            return geoserverItem
        except:
            QtGui.QApplication.restoreOverrideCursor()
            raise        
        
    def addQGisProjectToTree(self):        
        qgisItem = QtGui.QTreeWidgetItem()
        qgisItem.setText(0, "QGIS proyect") 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/qgis.png")
        qgisItem.setIcon(0, icon)
        layersItem = QtGui.QTreeWidgetItem()
        layersItem.setText(0, "Layers")
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        layersItem.setIcon(0, icon)
        layers = qgislayers.get_all_layers()
        for layer in layers:
            layerItem = QgsLayerItem(layer, self)            
            layersItem.addChild(layerItem)
        qgisItem.addChild(layersItem)
        groupsItem = QtGui.QTreeWidgetItem()
        groupsItem.setText(0, "Groups")
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        groupsItem.setIcon(0, icon)
        groups = qgislayers.get_groups()
        for group in groups:
            groupItem = QgsGroupItem(group, self)                        
            groupsItem.addChild(groupItem)
        qgisItem.addChild(groupsItem)
        stylesItem = QtGui.QTreeWidgetItem()
        stylesItem.setText(0, "Styles")
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        stylesItem.setIcon(0, icon)
        styles = qgislayers.get_all_layers()
        for style in styles:
            styleItem = QgsStyleItem(style, self)            
            stylesItem.addChild(styleItem)
        qgisItem.addChild(stylesItem)
        self.tree.addTopLevelItem(qgisItem)

    
    #========== menus and actions =====================
     
            
    def showTreePopupMenu(self,point):
        currentItem = self.tree.itemAt(point)                
        self.currentElementData = currentItem.data(0, QtCore.Qt.UserRole)
        self.currentElementText = currentItem.text(0)

        
        if hasattr(currentItem, "popupmenu"):
            publishStyleAction = QtGui.QAction("Publish style...", None)
            publishStyleAction.triggered.connect(self.publishStyle)
            currentItem.popupmenu(self.tree.mapToGlobal(point))

    



################################################################

class QgsTreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, explorer, icon = None, text = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element
        self.explorer = explorer         
        text = text if text is not None else util.name(element)
        self.setText(0, text)        
        if icon is not None:
            self.setIcon(0, icon)
    
    def selectCatalog(self):
        if len(self.explorer.catalogs) == 1:
            return self.explorer.catalogs[1]
        else:
            #TODO
            pass

class QgsLayerItem(QgsTreeItem): 
    def __init__(self, layer, explorer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        QgsTreeItem.__init__(self, layer, explorer, icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        publishLayerAction = QtGui.QAction("Publish layer", None)
        publishLayerAction.triggered.connect(self.publishLayer)
        menu.addAction(publishLayerAction)   
        createStoreFromLayerAction= QtGui.QAction("Create store from layer", None)
        createStoreFromLayerAction.triggered.connect(self.createStoreFromLayer)
        menu.addAction(createStoreFromLayerAction)                              
        menu.exec_(self.tree.mapToGlobal(point))    
        
    def createStoreFromLayer(self):
        pass
            
    def publishLayer(self):
        cat = self.selectCatalog()
        ogcat = OGCatalog(cat)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            ogcat.publish_layer(self.currentElementData, overwrite=True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()        
                
class QgsGroupItem(QgsTreeItem): 
    def __init__(self, group, explorer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        QgsTreeItem.__init__(self, group, explorer, icon)         

class QgsStyleItem(QgsTreeItem): 
    def __init__(self, layer, explorer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        QgsTreeItem.__init__(self, layer, explorer, icon, "Style of layer '" + layer.name() + "'")         
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        publishStyleAction = QtGui.QAction("Publish style...", None)
        publishStyleAction.triggered.connect(self.publishStyle)
        menu.addAction(publishStyleAction)                                
        menu.exec_(self.tree.mapToGlobal(point))          

    def publishStyle(self):
        cat = self.selectCatalog()
        ogcat = OGCatalog(cat)        
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            ogcat.publish_style(self.currentElementData, True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()      
                
class TreeContainerItem(QtGui.QTreeWidgetItem): 
    def __init__(self, text, icon = None): 
        QtGui.QTreeWidgetItem.__init__(self)                 
        self.setText(0, text)        
        if icon is not None:
            self.setIcon(0, icon)
            
class LayersItem(TreeContainerItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeContainerItem.__init__(self, "Layers", icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createLayerAction = QtGui.QAction("New layer...", None)
        createLayerAction.triggered.connect(self.createLayer)
        menu.addAction(createLayerAction) 
        menu.exec_(point)                                                                   
    
    def createLayer(self):
        pass    
    
            
class GroupsItem(TreeContainerItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeContainerItem.__init__(self, "Groups", icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createGroupAction = QtGui.QAction("New group...", None)
        createGroupAction.triggered.connect(self.createGroup)
        menu.addAction(createGroupAction)                                                            
        menu.exec_(point)   
    
    def createGroup(self):
        pass    
    
        
class WorkspacesItem(TreeContainerItem): 
    def __init__(self): 
        #icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeContainerItem.__init__(self, "Workspaces") 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createWorkspaceAction = QtGui.QAction("New workspace...", None)
        createWorkspaceAction.triggered.connect(self.createWorkspace)
        menu.addAction(createWorkspaceAction)                                                         
        menu.exec_(point)
    
    def createWorkspace(self):
        pass
    
class StylesItem(TreeContainerItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeContainerItem.__init__(self, "Styles", icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createStyleAction = QtGui.QAction("New style...", None)
        createStyleAction.triggered.connect(self.createStyle)
        menu.addAction(createStyleAction)            
        createStyleFromLayerAction = QtGui.QAction("New style from QGIS layer...", None)
        createStyleFromLayerAction.triggered.connect(self.createStyleFromLayer)
        menu.addAction(createStyleFromLayerAction)                                                                
        menu.exec_(point)
        
    def createStyle(self):
        pass   
        
    def createStyleFromLayer(self):
        pass    
                        
        
class GsTreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, icon = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element         
        self.setText(0, util.name(element))        
        if icon is not None:
            self.setIcon(0, icon)
        self.setData(0, QtCore.Qt.UserRole, element)          
        #self.setFlags(self.flags() & flags) 
        
    def parentCatalog(self, item):
        lastItem = item        
        while item is not None:
            data = lastItem.data(0, QtCore.Qt.UserRole)            
            if isinstance(data, Catalog):
                return data                
            lastItem = item
            item = item.parent()            
        return None         
                
class CatalogItem(GsTreeItem): 
    def __init__(self, catalog, name): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = catalog         
        self.setText(0, name)
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")        
        self.setIcon(0, icon)
        self.setData(0, QtCore.Qt.UserRole, catalog)
        
    def removeCatalog(self):
        pass            
    
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        removeCatalogAction = QtGui.QAction("Remove", None)
        removeCatalogAction.triggered.connect(self.removeCatalog)
        menu.addAction(removeCatalogAction)                                                     
        menu.exec_(point)
        
                        
class LayerItem(GsTreeItem): 
    def __init__(self, layer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        GsTreeItem.__init__(self, layer, icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        if isinstance(self.parent(), GroupItem):
            removeLayerFromGroupAction = QtGui.QAction("Remove layer from group", None)
            removeLayerFromGroupAction.triggered.connect(self.removeLayerFromGroup)
            menu.addAction(removeLayerFromGroupAction)                                                
        else:
            deleteLayerAction = QtGui.QAction("Delete", None)
            deleteLayerAction.triggered.connect(self.deleteLayer)
            menu.addAction(deleteLayerAction)                                
            addLayerAction = QtGui.QAction("Add to current QGIS project", None)
            addLayerAction.triggered.connect(self.addLayer)
            menu.addAction(addLayerAction)                                                               
        menu.exec_(point)   

    def addLayer(self):
        cat = OGCatalog(self.currentCatalog)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            cat.add_layer_to_project(self.currentElementData.typename)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        #TODO:update tree
        
    def deleteLayer(self):
        pass
            
    def removeLayerFromGroup(self):
        pass     
                  
class GroupItem(GsTreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        GsTreeItem.__init__(self, group, icon)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        deleteLayerGroupAction = QtGui.QAction("Delete", None)
        deleteLayerGroupAction.triggered.connect(self.deleteLayerGroup)
        menu.addAction(deleteLayerGroupAction)                                
        addLayerAction = QtGui.QAction("Add to current QGIS project", None)
        addLayerAction.triggered.connect(self.addLayer)
        menu.addAction(addLayerAction)                                                                                                             
        menu.exec_(point)        
        
    def deleteLayerGroup(self):
        pass   
    
    def addLayer(self):
        pass      
    

class StyleItem(GsTreeItem): 
    def __init__(self, style, is_default): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        GsTreeItem.__init__(self, style, icon)
        self.is_default = is_default
        name = style.name if not is_default else style.name + "[default style]"
        self.setText(0, name)   

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        if isinstance(self.parent, LayerItem):
            setAsDefaultStyleAction = QtGui.QAction("Set as default style", None)
            setAsDefaultStyleAction.triggered.connect(self.setAsDefaultStyle)
            menu.addAction(setAsDefaultStyleAction)  
            removeStyleFromLayerAction = QtGui.QAction("Remove style from layer", None)
            removeStyleFromLayerAction.triggered.connect(self.removeStyleFromLayer)
            menu.addAction(removeStyleFromLayerAction)                 
        else:                      
            deleteStyleAction = QtGui.QAction("Delete", None)
            deleteStyleAction.triggered.connect(self.deleteStyle)
            menu.addAction(deleteStyleAction)                                                                               
        menu.exec_(point)        
    
    def removeStyleFromLayer(self):
        pass
    
    def setAsDefaultStyle(self):
        pass
    
    def deleteStyle(self):
        pass
                    
          
class WorkspaceItem(GsTreeItem): 
    def __init__(self, workspace):         
        GsTreeItem.__init__(self, workspace)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        setAsDefaultAction = QtGui.QAction("Set as default workspace...", None)
        setAsDefaultAction.triggered.connect(self.setAsDefaultWorkspace)
        menu.addAction(setAsDefaultAction)                                         
        deleteWorkspaceAction = QtGui.QAction("Delete", None)
        deleteWorkspaceAction.triggered.connect(self.deleteWorkspace)
        menu.addAction(deleteWorkspaceAction)                                                
        menu.exec_(point)
    
    def deleteWorkspace(self):
        pass
    
    
    def setAsDefaultWorkspace(self):
        pass
            
                             
class StoreItem(GsTreeItem): 
    def __init__(self, store):         
        GsTreeItem.__init__(self, store)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        deleteStoreAction = QtGui.QAction("Delete", None)
        deleteStoreAction.triggered.connect(self.deleteStore)
        menu.addAction(deleteStoreAction)        
        menu.exec_(point)                         

    def deleteStore(self):
        pass

class ResourceItem(GsTreeItem): 
    def __init__(self, resource):         
        GsTreeItem.__init__(self, resource)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        publishResourceAction = QtGui.QAction("Publish...", None)
        publishResourceAction.triggered.connect(self.publishResource)
        menu.addAction(publishResourceAction)
        addResourceAsLayerAction = QtGui.QAction("Add to current QGIS project", None)
        addResourceAsLayerAction.triggered.connect(self.addResourceAsLayer)
        menu.addAction(addResourceAsLayerAction)        
        menu.exec_(point)        
    
    def addResourceAsLayer(self):
        pass
                   
    def publishResource(self):
        pass
        
                 
