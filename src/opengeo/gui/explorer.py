from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from opengeo.qgis import layers as qgislayers
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogdialog import DefineCatalogDialog
from opengeo.geoserver.catalog import Catalog
import os
from opengeo.core import util
from opengeo.gui.groupdialog import LayerGroupDialog
from opengeo.gui.workspacedialog import DefineWorkspaceDialog
from opengeo.gui.styledialog import StyleFromLayerDialog, AddStyleToLayerDialog


class GeoServerExplorer(QtGui.QDialog):
    
    gsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
    layerIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
    groupIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
    styleIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
    
    def __init__(self, parent = None):
        super(GeoServerExplorer, self).__init__()        
        self.catalogs = {}
        self.initGui()
        
    def initGui(self):      
        self.resize(400, 600) 
        self.setWindowTitle('GeoServer explorer')
        self.splitter = QtGui.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.verticalLayout = QtGui.QVBoxLayout(self.splitter)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)         
        self.toolbar = QtGui.QToolBar()
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
        self.toolbar.addAction(icon, "Add Geoserver catalog", self.addGeoServerCatalog)  
        self.verticalLayout.addWidget(self.toolbar)                         
        self.tree = QtGui.QTreeWidget()         
        self.tree.itemClicked.connect(self.treeItemClicked)        
        self.tree.setColumnCount(1)            
        self.tree.header().hide()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showTreePopupMenu)
        self.fillTree()                                                                                  
        self.verticalLayout.addWidget(self.tree)         
        self.log = QtGui.QTextEdit(self.splitter)                
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setMargin(0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.splitter)       

    
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
            name = dlg.getName()
            #TODO Check name does not exist already           
            self.catalogs[name] = cat
            item = self.getGeoServerCatalogItem(cat, name)
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
            workspacesItem = WorkspacesItem(cat)   
            defaultWorkspace = cat.get_default_workspace()
            defaultWorkspace.fetch()
            defaultName = defaultWorkspace.dom.find('name').text             
            workspaces = cat.get_workspaces()
            for workspace in workspaces:
                workspaceItem = WorkspaceItem(workspace)
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
            layersItem = LayersItem(cat)            
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
            groupsItem = GroupsItem(cat)
            groups = cat.get_layergroups()
            for group in groups:
                groupItem = GroupItem(group)                
                for layer in group.layers:
                    layerItem = LayerItem(layersDict[layer])                    
                    groupItem.addChild(layerItem)
                groupsItem.addChild(groupItem)            
            geoserverItem.addChild(groupsItem)
            stylesItem = StylesItem(cat)            
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

      
    def showTreePopupMenu(self,point):
        currentItem = self.tree.itemAt(point)                

        if hasattr(currentItem, "popupmenu"):
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
            return self.explorer.catalogs.values()[0]
        else:
            item, ok = QtGui.QInputDialog.getItem(self,
                u"Catalog selection",
                u"Select a destination catalog",
                self.catalogs.keys(),
                editable = False)
            if ok:
                return self.catalogs[item]
            else:
                return None
            

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
        menu.exec_(point)    
        
    def createStoreFromLayer(self):
        cat = self.selectCatalog()
        if cat is None:
            return
        ogcat = OGCatalog(cat)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            ogcat.create_store(self.element, overwrite=True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()  
            
    def publishLayer(self):
        cat = self.selectCatalog()
        if cat is None:
            return
        ogcat = OGCatalog(cat)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            ogcat.publish_layer(self.element, overwrite=True)
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
        menu.exec_(point)          

    def publishStyle(self):
        cat = self.selectCatalog()
        if cat is None:
            return
        ogcat = OGCatalog(cat)        
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            ogcat.publish_style(self.element, overwrite = True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()      
                
class TreeContainerItem(QtGui.QTreeWidgetItem): 
    def __init__(self, text, catalog, icon = None): 
        QtGui.QTreeWidgetItem.__init__(self)                 
        self.catalog = catalog
        self.setText(0, text)        
        if icon is not None:
            self.setIcon(0, icon)
            
class LayersItem(TreeContainerItem): 
    def __init__(self, catalog): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeContainerItem.__init__(self, "Layers", catalog, icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createLayerAction = QtGui.QAction("New layer...", None)
        createLayerAction.triggered.connect(self.createLayer)
        menu.addAction(createLayerAction) 
        menu.exec_(point)                                                                   
    
    def createLayer(self):
        pass
        #=======================================================================
        # dlg = LayerCreationDialog(self.catalog)
        # dlg.exec_()
        # layer = dlg.getLayer()
        # if layer is not None:
        #=======================================================================
                
    
            
class GroupsItem(TreeContainerItem): 
    def __init__(self, catalog): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeContainerItem.__init__(self, "Groups", catalog, icon) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createGroupAction = QtGui.QAction("New group...", None)
        createGroupAction.triggered.connect(self.createGroup)
        menu.addAction(createGroupAction)                                                            
        menu.exec_(point)   
    
    def createGroup(self):
        dlg = LayerGroupDialog(self.catalog)
        dlg.exec_()
        group = dlg.group
        if group is not None:
            self.catalog.save(group)   
    
        
class WorkspacesItem(TreeContainerItem): 
    def __init__(self, catalog): 
        #icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeContainerItem.__init__(self, "Workspaces", catalog) 

    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        createWorkspaceAction = QtGui.QAction("New workspace...", None)
        createWorkspaceAction.triggered.connect(self.createWorkspace)
        menu.addAction(createWorkspaceAction)                                                         
        menu.exec_(point)
    
    def createWorkspace(self):
        dlg = DefineWorkspaceDialog() 
        dlg.exec_()            
        if dlg.name is not None:
            self.catalog.create_workspace(dlg.name, dlg.uri)
    
class StylesItem(TreeContainerItem): 
    def __init__(self, catalog): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeContainerItem.__init__(self, "Styles", catalog, icon) 

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
        dlg = StyleFromLayerDialog()
        dlg.exec_()      
        if dlg.layer is not None:
            ogcat = OGCatalog(self.catalog)        
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
            try:
                ogcat.publish_style(dlg.layer, dlg.name, True)
            finally:
                QtGui.QApplication.restoreOverrideCursor()     
                        
        
class GsTreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, icon = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element         
        self.setText(0, util.name(element))        
        if icon is not None:
            self.setIcon(0, icon)
        self.setData(0, QtCore.Qt.UserRole, element)          
        #self.setFlags(self.flags() & flags) 
        
    def parentCatalog(self):
        item = self
        lastItem = self        
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
            layers = self.parent().element.layers
            count = len(layers)
            idx = layers.index(self.element.name)
            removeLayerFromGroupAction = QtGui.QAction("Remove layer from group", None)            
            removeLayerFromGroupAction.setEnabled(count > 1)
            removeLayerFromGroupAction.triggered.connect(self.removeLayerFromGroup)
            menu.addAction(removeLayerFromGroupAction)                                                
            moveLayerUpInGroupAction = QtGui.QAction("Move up", None)            
            moveLayerUpInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerUpInGroupAction.triggered.connect(self.moveLayerUpInGroup)
            menu.addAction(moveLayerUpInGroupAction)
            moveLayerDownInGroupAction = QtGui.QAction("Move down", None)            
            moveLayerDownInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerDownInGroupAction.triggered.connect(self.moveLayerDownInGroup)
            menu.addAction(moveLayerDownInGroupAction)
            moveLayerToFrontInGroupAction = QtGui.QAction("Move to front", None)            
            moveLayerToFrontInGroupAction.setEnabled(count > 1 and idx > 0)
            moveLayerToFrontInGroupAction.triggered.connect(self.moveLayerToFrontInGroup)
            menu.addAction(moveLayerToFrontInGroupAction)
            moveLayerToBackInGroupAction = QtGui.QAction("Move to back", None)            
            moveLayerToBackInGroupAction.setEnabled(count > 1 and idx < count - 1)
            moveLayerToBackInGroupAction.triggered.connect(self.moveLayerToBackInGroup)
            menu.addAction(moveLayerToBackInGroupAction)
        else:
            addStyleToLayerAction = QtGui.QAction("Add style to layer", None)
            addStyleToLayerAction.triggered.connect(self.addStyleToLayer)                    
            menu.addAction(addStyleToLayerAction)   
            deleteLayerAction = QtGui.QAction("Delete", None)
            deleteLayerAction.triggered.connect(self.deleteLayer)
            menu.addAction(deleteLayerAction)                                
            addLayerAction = QtGui.QAction("Add to current QGIS project", None)
            addLayerAction.triggered.connect(self.addLayer)
            menu.addAction(addLayerAction)                                                               
        menu.exec_(point)   

    
    def addStyleToLayer(self):
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
                cat.save(layer)
            else:
                styles.append(dlg.style)
                layer.styles = styles 
                for style in layer.styles:
                    print style
                cat.save(layer)            
            
    def addLayer(self):
        cat = OGCatalog(self.parentCatalog())
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            cat.add_layer_to_project(self.element.name)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        #TODO:update tree
        
    def deleteLayer(self):
        self.parentCatalog().delete(self.element)
            
    def removeLayerFromGroup(self):
        group = self.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.element.name)
        del layers[idx]
        del styles[idx]
        group.dirty.update(layers = layers, styles = styles)
        self.parentCatalog().save(group)

    def moveLayerDownInGroup(self):
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
        self.parentCatalog().save(group)  
    
    def moveLayerToFrontInGroup(self):
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
        self.parentCatalog().save(group)  
    
    def moveLayerToBackInGroup(self):
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
        self.parentCatalog().save(group)
                     
    def moveLayerUpInGroup(self):
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
        self.parentCatalog().save(group)                         
                  
class GroupItem(GsTreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        GsTreeItem.__init__(self, group, icon)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        editLayerGroupAction = QtGui.QAction("Edit...", None)
        editLayerGroupAction.triggered.connect(self.editLayerGroup)
        menu.addAction(editLayerGroupAction)     
        deleteLayerGroupAction = QtGui.QAction("Delete", None)
        deleteLayerGroupAction.triggered.connect(self.deleteLayerGroup)
        menu.addAction(deleteLayerGroupAction)                                
        addLayerAction = QtGui.QAction("Add to current QGIS project", None)
        addLayerAction.triggered.connect(self.addLayer)
        menu.addAction(addLayerAction)                                                                                                             
        menu.exec_(point)        
        
    def deleteLayerGroup(self):
        self.parentCatalog().delete(self.element)   
    
    def editLayerGroup(self):
        cat = self.parentCatalog()        
        dlg = LayerGroupDialog(cat, self.element)
        dlg.exec_()
        group = dlg.group
        if group is not None:
            cat.save(group)   
    
    def addLayer(self):
        pass      
    

class StyleItem(GsTreeItem): 
    def __init__(self, style, isDefault): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        GsTreeItem.__init__(self, style, icon)
        self.isDefault = isDefault
        name = style.name if not isDefault else style.name + " [default style]"
        self.setText(0, name)   

    def popupmenu(self, point):
        menu = QtGui.QMenu()         
        if isinstance(self.parent(), LayerItem):
            setAsDefaultStyleAction = QtGui.QAction("Set as default style", None)
            setAsDefaultStyleAction.triggered.connect(self.setAsDefaultStyle)
            setAsDefaultStyleAction.setEnabled(not self.isDefault)
            menu.addAction(setAsDefaultStyleAction)  
            removeStyleFromLayerAction = QtGui.QAction("Remove style from layer", None)
            removeStyleFromLayerAction.triggered.connect(self.removeStyleFromLayer)
            removeStyleFromLayerAction.setEnabled(not self.isDefault)            
            menu.addAction(removeStyleFromLayerAction)                           
        else:                      
            deleteStyleAction = QtGui.QAction("Delete", None)
            deleteStyleAction.triggered.connect(self.deleteStyle)
            menu.addAction(deleteStyleAction)                                                                               
        menu.exec_(point)        
    
    def removeStyleFromLayer(self):
        layer = self.parent().element
        default = layer.default_style
        styles = layer.styles
        styles = [style for style in styles if style.name != self.element.name]
        styles.append(default)        
        layer.styles = styles 
        self.parentCatalog().save(layer)
    
    def setAsDefaultStyle(self):
        layer = self.parent().element
        default = layer.default_style
        styles = layer.styles
        styles = [style for style in styles if style.name != self.element.name]
        styles.append(default)
        layer.default_style = self.element
        layer.styles = styles 
        self.parentCatalog().save(layer)
    
    def deleteStyle(self):
        self.parentCatalog().delete(self.element) 
                    
          
class WorkspaceItem(GsTreeItem): 
    def __init__(self, workspace, isDefault):         
        GsTreeItem.__init__(self, workspace)
        self.isDefault = isDefault        
        name = workspace.name if not isDefault else workspace.name + " [default workspace]"
        self.setText(0, name)
        
    def popupmenu(self, point):
        menu = QtGui.QMenu() 
        setAsDefaultAction = QtGui.QAction("Set as default workspace...", None)
        setAsDefaultAction.triggered.connect(self.setAsDefaultWorkspace)
        setAsDefaultAction.setEnabled(not self.isDefault)
        menu.addAction(setAsDefaultAction)                                         
        deleteWorkspaceAction = QtGui.QAction("Delete", None)
        deleteWorkspaceAction.triggered.connect(self.deleteWorkspace)
        menu.addAction(deleteWorkspaceAction)                                                
        menu.exec_(point)
    
    def deleteWorkspace(self):
        self.parentCatalog().delete(self.element) 
    
    def setAsDefaultWorkspace(self):
        self.parentCatalog().set_default_workspace(self.element.name)
            
                             
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
        self.parentCatalog().delete(self.element) 

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
        
                 
