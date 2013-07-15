from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from opengeo.qgis import layers as qgislayers
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogdialog import DefineCatalogDialog
import os
from opengeo.core import util
from opengeo.gui.groupdialog import LayerGroupDialog
from opengeo.gui.workspacedialog import DefineWorkspaceDialog
from opengeo.gui.styledialog import StyleFromLayerDialog, AddStyleToLayerDialog,\
    PublishStyleDialog
from opengeo.gui.explorerthread import ExplorerThread
from opengeo.gui.layerdialog import PublishLayerDialog, PublishLayersDialog


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
        self.tree = QtGui.QTreeWidget() 
        self.tree.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)        
        self.tree.itemClicked.connect(self.treeItemClicked)        
        self.tree.setColumnCount(1)            
        self.tree.header().hide()
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showTreePopupMenu)
        self.fillTree()                                                                                  
        self.verticalLayout.addWidget(self.tree)         
        self.log = QtGui.QTextEdit(self.splitter) 
        self.progress = QtGui.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)                       
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setMargin(0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.splitter)
        self.layout.addWidget(self.progress)       

    
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
            geoserverItem = GsCatalogItem(cat, name)
            geoserverItem.populate()
            QtGui.QApplication.restoreOverrideCursor()
            self.setInfo("Catalog '" + name + "' correctly created")
            return geoserverItem
        except Exception, e:
            QtGui.QApplication.restoreOverrideCursor()
            self.setInfo("Could not create catalog:" + str(e), True)
            #raise        
        
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
            layerItem = QgsLayerItem(layer)            
            layersItem.addChild(layerItem)
        qgisItem.addChild(layersItem)
        groupsItem = QtGui.QTreeWidgetItem()
        groupsItem.setText(0, "Groups")
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        groupsItem.setIcon(0, icon)
        groups = qgislayers.get_groups()
        for group in groups:
            groupItem = QgsGroupItem(group)                        
            groupsItem.addChild(groupItem)
        qgisItem.addChild(groupsItem)
        stylesItem = QtGui.QTreeWidgetItem()
        stylesItem.setText(0, "Styles")
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        stylesItem.setIcon(0, icon)
        styles = qgislayers.get_all_layers()
        for style in styles:
            styleItem = QgsStyleItem(style)            
            stylesItem.addChild(styleItem)
        qgisItem.addChild(stylesItem)
        self.tree.addTopLevelItem(qgisItem)

    def getSelectionTypes(self):
        items = self.tree.selectedItems()
        return set([type(item) for item in items])  

    def showTreePopupMenu(self,point):
        allTypes = self.getSelectionTypes()                
        if len(allTypes) != 1:
            return 
        items = self.tree.selectedItems()
        if len(items) > 1:
            self.showMultipleSelectionPopupMenu(point)
        else:
            self.showSingleSelectionPopupMenu(point)
            
    def showMultipleSelectionPopupMenu(self, point):        
        self.currentItem = self.tree.itemAt(point)  
        point = self.tree.mapToGlobal(point)
        menu = QtGui.QMenu()             
        if isinstance(self.currentItem, QgsLayerItem):                                    
            publishLayersAction = QtGui.QAction("Publish...", None)
            publishLayersAction.triggered.connect(self.publishLayers)
            menu.addAction(publishLayersAction)   
            createStoresFromLayersAction= QtGui.QAction("Create stores from layers...", None)
            createStoresFromLayersAction.triggered.connect(self.createStoresFromLayers)
            menu.addAction(createStoresFromLayersAction)  
            menu.exec_(point)    
        if isinstance(self.currentItem, GsLayerItem):                                    
            deleteLayersAction = QtGui.QAction("Delete", None)
            deleteLayersAction.triggered.connect(self.deleteLayers)
            menu.addAction(deleteLayersAction)           
            menu.exec_(point)                         
                
    def showSingleSelectionPopupMenu(self, point):        
        self.currentItem = self.tree.itemAt(point)     
        menu = QtGui.QMenu()
        if isinstance(self.currentItem, TreeItem) and hasattr(self.currentItem, 'populate'):            
            refreshAction = QtGui.QAction("Refresh", None)
            refreshAction.triggered.connect(self.currentItem.refreshContent)
            menu.addAction(refreshAction) 
        point = self.tree.mapToGlobal(point)               
        if isinstance(self.currentItem, QgsLayerItem):                        
            publishLayerAction = QtGui.QAction("Publish...", None)
            publishLayerAction.triggered.connect(self.publishLayer)
            menu.addAction(publishLayerAction)   
            createStoreFromLayerAction= QtGui.QAction("Create store from layer...", None)
            createStoreFromLayerAction.triggered.connect(self.createStoreFromLayer)
            menu.addAction(createStoreFromLayerAction)                              
            #menu.exec_(point)   
        elif isinstance(self.currentItem, QgsStyleItem):                     
            publishStyleAction = QtGui.QAction("Publish...", None)
            publishStyleAction.triggered.connect(self.publishStyle)
            menu.addAction(publishStyleAction)                                
            #menu.exec_(point)    
        elif isinstance(self.currentItem, GsStylesItem):     
            createStyleFromLayerAction = QtGui.QAction("New style from QGIS layer...", None)
            createStyleFromLayerAction.triggered.connect(self.createStyleFromLayer)
            menu.addAction(createStyleFromLayerAction)                                                                
            #menu.exec_(point)
        elif isinstance(self.currentItem, GsWorkspacesItem):                    
            createWorkspaceAction = QtGui.QAction("New workspace...", None)
            createWorkspaceAction.triggered.connect(self.createWorkspace)
            menu.addAction(createWorkspaceAction)                                                         
            #menu.exec_(point)
        elif isinstance(self.currentItem, GsGroupsItem):    
            createGroupAction = QtGui.QAction("New group...", None)
            createGroupAction.triggered.connect(self.createGroup)
            menu.addAction(createGroupAction)                                                            
            #menu.exec_(point) 
        elif isinstance(self.currentItem, GsLayerItem):
            if isinstance(self.currentItem.parent(), GsGroupItem):
                layers = self.currentItem.parent().element.layers
                count = len(layers)
                idx = layers.index(self.currentItem.element.name)
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
                addStyleToLayerAction = QtGui.QAction("Add style to layer...", None)
                addStyleToLayerAction.triggered.connect(self.addStyleToLayer)                    
                menu.addAction(addStyleToLayerAction)   
                deleteLayerAction = QtGui.QAction("Delete", None)
                deleteLayerAction.triggered.connect(self.deleteLayers)
                menu.addAction(deleteLayerAction)                                
                addLayerAction = QtGui.QAction("Add to current QGIS project", None)
                addLayerAction.triggered.connect(self.addLayerToProject)
                menu.addAction(addLayerAction)
            #menu.exec_(point)              
        elif isinstance(self.currentItem, GsGroupItem):    
            editLayerGroupAction = QtGui.QAction("Edit...", None)
            editLayerGroupAction.triggered.connect(self.editLayerGroup)
            menu.addAction(editLayerGroupAction)     
            deleteLayerGroupAction = QtGui.QAction("Delete", None)
            deleteLayerGroupAction.triggered.connect(self.deleteLayerGroup)
            menu.addAction(deleteLayerGroupAction)                                                                                                                                          
            #menu.exec_(point)     
        elif isinstance(self.currentItem, GsCatalogItem):                        
            removeCatalogAction = QtGui.QAction("Remove", None)
            removeCatalogAction.triggered.connect(self.removeCatalog)
            menu.addAction(removeCatalogAction)                                                     
            #menu.exec_(point)
        elif isinstance(self.currentItem, GsStyleItem):
            if isinstance(self.currentItem.parent(), GsLayerItem):
                setAsDefaultStyleAction = QtGui.QAction("Set as default style", None)
                setAsDefaultStyleAction.triggered.connect(self.setAsDefaultStyle)
                setAsDefaultStyleAction.setEnabled(not self.currentItem.isDefault)
                menu.addAction(setAsDefaultStyleAction)  
                removeStyleFromLayerAction = QtGui.QAction("Remove style from layer", None)
                removeStyleFromLayerAction.triggered.connect(self.removeStyleFromLayer)
                removeStyleFromLayerAction.setEnabled(not self.currentItem.isDefault)            
                menu.addAction(removeStyleFromLayerAction)                           
            else:                      
                deleteStyleAction = QtGui.QAction("Delete", None)
                deleteStyleAction.triggered.connect(self.deleteStyle)
                menu.addAction(deleteStyleAction)
            menu.exec_(point)  
        elif isinstance(self.currentItem, GsWorkspaceItem):                     
            setAsDefaultAction = QtGui.QAction("Set as default workspace", None)
            setAsDefaultAction.triggered.connect(self.setAsDefaultWorkspace)
            setAsDefaultAction.setEnabled(not self.currentItem.isDefault)
            menu.addAction(setAsDefaultAction)                                         
            deleteWorkspaceAction = QtGui.QAction("Delete", None)
            deleteWorkspaceAction.triggered.connect(self.deleteWorkspace)
            menu.addAction(deleteWorkspaceAction)                                                
            #menu.exec_(point)
        elif isinstance(self.currentItem, GsStoreItem):       
            deleteStoreAction = QtGui.QAction("Delete", None)
            deleteStoreAction.triggered.connect(self.deleteStore)
            menu.addAction(deleteStoreAction)        
            #menu.exec_(point) 
        elif isinstance(self.currentItem, GsResourceItem):        
            addResourceAsLayerAction = QtGui.QAction("Add to current QGIS project", None)
            addResourceAsLayerAction.triggered.connect(self.addResourceAsLayer)
            menu.addAction(addResourceAsLayerAction)                        
            deleteResourceAction = QtGui.QAction("Delete", None)
            deleteResourceAction.triggered.connect(self.deleteResource)
            menu.addAction(deleteResourceAction)        
            #menu.exec_(point) 
        
        if not self.catalogs:
            for action in menu.actions():
                action.setEnabled(False)
            
        if isinstance(self.currentItem, TreeItem):
            menu.exec_(point)        
        elif self.currentItem.text(0) == "GeoServer catalogs":
            addCatalogAction = QtGui.QAction("Add GeoServer catalog", None)
            addCatalogAction.triggered.connect(self.addGeoServerCatalog)
            menu.addAction(addCatalogAction)        
            menu.exec_(point)
  
            
########### ACTIONS#################################

    def run(self, command, okmsg, refresh, *params):                                
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))        
        thread = ExplorerThread(command, *params)                
        def finish():
            QtGui.QApplication.restoreOverrideCursor()
            for item in refresh:
                item.refreshContent()
            self.setInfo(okmsg)
        def error(msg):
            QtGui.QApplication.restoreOverrideCursor()
            self.setInfo(msg, True)            
        thread.finish.connect(finish)
        thread.error.connect(error)                                         
        thread.start()
        thread.wait()
        
    def setInfo(self, msg, error = False):
        if error:
            self.log.append('<ul><li><span style="color:red">ERROR: ' + msg + '</span></li></ul>')
        else:
            self.log.append('<ul><li><span style="color:blue">INFO: ' + msg + '</span></li></ul>')
            
    def findAllItems(self, element):
        allItems = []
        iterator = QtGui.QTreeWidgetItemIterator(self.tree)
        value = iterator.value()
        while value:
            if (hasattr(value, 'element') 
                        and value.element == element):
                    allItems.append(value)                
            iterator += 1
            value = iterator.value()
        return allItems

    def deleteStore(self):
        self.run(self.currentItem.parentCatalog().delete,
                 "Store '" + self.currentItem.element.name + "' correctly deleted",
                 [self.currentItem.parent()], 
                 self.currentItem.element) 
        
    def deleteResource(self):
        self.run(self.currentItem.parentCatalog().delete,
                 "Resource '" + self.currentItem.element.name + "' correctly deleted",
                 [self.currentItem.parent()], 
                 self.currentItem.element)         
        
    def deleteWorkspace(self):
        self.run(self.currentItem.parentCatalog().delete,
                 "Workspace '" + self.currentItem.element.name + "' correctly deleted",
                 [self.currentItem.parent()],
                 self.currentItem.element)         
    
    def setAsDefaultWorkspace(self):
        self.run(self.currentItem.parentCatalog().set_default_workspace, 
                 "Workspace '" + self.currentItem.element.name + "' set as default workspace",
                 [self.currentItem.parent()],
                 self.currentItem.element.name)

    def removeStyleFromLayer(self):
        layer = self.currentItem.parent().element        
        styles = layer.styles
        styles = [style for style in styles if style.name != self.currentItem.element.name]            
        layer.styles = styles 
        self.run(self.currentItem.parentCatalog().save, 
                "Style '" + self.currentItem.element.name + "' removed from layer '" + layer.name, 
                self.findAllItems(self.currentItem.parent().element),
                layer)
    
    def setAsDefaultStyle(self):
        layer = self.currentItem.parent().element        
        styles = layer.styles
        styles = [style for style in styles if style.name != self.currentItem.element.name]
        default = layer.default_style
        if default is not None:
            styles.append(default)
        layer.default_style = self.currentItem.element
        layer.styles = styles 
        self.run(self.currentItem.parentCatalog().save, 
                "Style '" + self.currentItem.element.name + "' set as default style for layer '" + layer.name + "'", 
                self.findAllItems(self.currentItem.parent().element),
                layer)        
    
    def addStyleToLayer(self):
        cat = self.currentItem.parentCatalog()
        dlg = AddStyleToLayerDialog(cat)
        dlg.exec_()
        if dlg.style is not None:
            layer = self.currentItem.element
            styles = layer.styles            
            if dlg.default:
                default = layer.default_style
                styles.append(default)
                layer.styles = styles
                layer.default_style = dlg.style                 
            else:
                styles.append(dlg.style)
                layer.styles = styles 
            self.run(cat.save, 
                     "Style '" + dlg.style.name + "' correctly added to layer '" + layer.name + "'",
                     [self.currentItem],
                     layer)    
            
    def deleteStyle(self):
        self.run(self.currentItem.parentCatalog().delete,
                 "Style '" + self.currentItem.element.name + "' correctly deleted",
                 [self.currentItem.parent()], 
                 self.currentItem.element)          
                            
    def deleteLayerGroup(self):
        self.run(self.currentItem.parentCatalog().delete,
                 "Layer group '" + self.currentItem.element.name + "' correctly deleted", 
                 [self.currentItem.parent()],
                 self.currentItem.element)            
    
    def editLayerGroup(self):
        cat = self.currentItem.parentCatalog()        
        dlg = LayerGroupDialog(cat, self.currentItem.element)
        dlg.exec_()
        group = dlg.group
        if group is not None:
            self.run(cat.save, "Layer group '" + self.currentItem.name + "' correctly edited", group)   
    
        
            
    def addLayerToProject(self):
        cat = OGCatalog(self.currentItem.parentCatalog())                 
        self.run(cat.add_layer_to_project, 
                 "Layer '" + self.currentItem.element.name + "' correctly added to QGIS project", 
                 [],
                 self.currentItem.element.name)
        
    def deleteLayers(self):        
        selected = self.tree.selectedItems()
        layers = [item.element for item in selected]
        parents = set(item.parent() for item in selected)                
        self.progress.setMaximum(len(layers))
        progress = 0        
        for layer in layers:
            self.progress.setValue(progress)                                        
            self.run(self.currentItem.parentCatalog().delete,
                 "Layer '" + self.currentItem.element.name + "' correctly deleted",
                 list(parents), 
                 layer)  
            progress += 1
        self.progress.setValue(progress)
                
            
    def removeLayerFromGroup(self):
        group = self.currentItem.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.currentItem.element.name)
        del layers[idx]
        del styles[idx]
        group.dirty.update(layers = layers, styles = styles)
        self.run(self.currentItem.parentCatalog().save, 
                 "Layer '" + self.currentItem.element.name + "' correctly removed from group '" + group.name +"'",
                 [self.currentItem.parent()],
                 group)

    def moveLayerDownInGroup(self):
        group = self.currentItem.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.currentItem.element.name)
        tmp = layers [idx + 1]
        layers[idx + 1] = layers[idx]
        layers[idx] = tmp  
        tmp = styles [idx + 1]
        styles[idx + 1] = styles[idx]
        styles[idx] = tmp          
        group.dirty.update(layers = layers, styles = styles)
        self.run(self.currentItem.parentCatalog().save, 
                 "Layer '" + self.currentItem.element.name + "' correctly moved down in group '" + group.name +"'",
                 [self.currentItem.parent()],
                 group)        
    
    def moveLayerToFrontInGroup(self):
        group = self.currentItem.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.currentItem.element.name)
        tmp = layers[idx]
        del layers[idx]
        layers.insert(0, tmp)        
        tmp = styles [idx]
        del styles[idx]
        styles.insert(0, tmp)          
        group.dirty.update(layers = layers, styles = styles)
        self.run(self.currentItem.parentCatalog().save, 
                 "Layer '" + self.currentItem.element.name + "' correctly moved to front in group '" + group.name +"'",
                 [self.currentItem.parent()],
                 group)
    
    def moveLayerToBackInGroup(self):
        group = self.currentItem.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.currentItem.element.name)
        tmp = layers[idx]
        del layers[idx]
        layers.append(tmp)        
        tmp = styles [idx]
        del styles[idx]
        styles.append(tmp)          
        group.dirty.update(layers = layers, styles = styles)
        self.run(self.currentItem.parentCatalog().save, 
                 "Layer '" + self.currentItem.element.name + "' correctly moved to back in group '" + group.name +"'",
                 [self.currentItem.parent()],
                 group)
                     
    def moveLayerUpInGroup(self):
        group = self.currentItem.parent().element
        layers = group.layers
        styles = group.styles
        idx = group.layers.index(self.currentItem.element.name)
        tmp = layers [idx - 1]
        layers[idx - 1] = layers[idx]
        layers[idx] = tmp  
        tmp = styles [idx - 1]
        styles[idx - 1] = styles[idx]
        styles[idx] = tmp          
        group.dirty.update(layers = layers, styles = styles)
        self.run(self.currentItem.parentCatalog().save, 
                 "Layer '" + self.currentItem.element.name + "' correctly moved up in group '" + group.name +"'",
                 [self.currentItem.parent()],
                 group)
                
    def removeCatalog(self):
        del self.catalogs[self.currentItem.text(0)]
        parent = self.currentItem.parent()        
        parent.takeChild(parent.indexOfChild(self.currentItem))   
        
    def createStyleFromLayer(self):  
        dlg = StyleFromLayerDialog(self.catalogs.keys())
        dlg.exec_()      
        if dlg.layer is not None:
            ogcat = OGCatalog(self.catalogs[dlg.catalog])        
            self.run(ogcat.publish_style, 
                     "Style correctly created from layer '" + dlg.layer + "'",
                     [self.currentItem],
                     dlg.layer, dlg.name, True)
            
                
    def createWorkspace(self):
        dlg = DefineWorkspaceDialog() 
        dlg.exec_()            
        if dlg.name is not None:
            self.run(self.currentItem.parentCatalog().create_workspace, 
                    "Workspace '" + dlg.name + "' correctly created",
                    [self.currentItem],
                    dlg.name, dlg.uri)
    
    
    def createGroup(self):
        dlg = LayerGroupDialog(self.currentItem.parentCatalog())
        dlg.exec_()
        group = dlg.group
        if group is not None:
            self.run(self.currentItem.parentCatalog().save,
                     "Group '" + group.name + "' correctly created",
                     [self.currentItem],
                     group)


    def createStoreFromLayer(self):
        dlg = PublishLayerDialog(self.catalogs)
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = self.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        self.run(ogcat.create_store,
                 "Store correctly created from layer '" + self.currentItem.element.name() + "'",
                 toUpdate,
                 self.currentItem.element, dlg.workspace, True)
        
    def createStoresFromLayers(self):
        pass        
            
    def publishLayer(self):
        dlg = PublishLayerDialog(self.catalogs)
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog  
        ogcat = OGCatalog(cat)
        catItem = self.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        self.run(ogcat.publish_layer,
                 "Layer correctly published from layer '" + self.currentItem.element.name() + "'",
                 toUpdate,
                 self.currentItem.element, dlg.workspace, True)

    def publishLayers(self):
        selected = self.tree.selectedItems()
        layers = [item.element for item in selected]        
        dlg = PublishLayersDialog(self.catalogs, layers)
        dlg.exec_()     
        topublish  = dlg.topublish
        if topublish is None:
            return
        self.progress.setMaximum(len(topublish))
        progress = 0        
        for layer, catalog, workspace in topublish:
            self.progress.setValue(progress)            
            ogcat = OGCatalog(catalog)                 
            self.run(ogcat.publish_layer,
                     "Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1
        self.progress.setValue(progress)
            
        #TODO update changed trees
                           

    def publishStyle(self):
        dlg = PublishStyleDialog(self.catalogs.keys())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = self.catalogs[dlg.catalog]  
        ogcat = OGCatalog(cat)
        catItem = self.findAllItems(cat)[0]
        toUpdate = []
        for idx in range(catItem.childCount()):
            subitem = catItem.child(idx)
            if isinstance(subitem, GsStylesItem):
                toUpdate.append(subitem)
                break                
        self.run(ogcat.publish_style,
                 "Style correctly published from layer '" + self.currentItem.element.name() + "'",
                 toUpdate,
                 self.currentItem.element, dlg.name, True)
         
            
    def addResourceAsLayer(self):
        cat = OGCatalog(self.currentItem.parentCatalog())                 
        self.run(cat.add_layer_to_project, 
                 "Layer '" + self.currentItem.element.name + "' correctly added to QGIS project from resource", 
                 [self.currentItem.element],
                 self.currentItem.element.name)
    #===========================================================================
    #               
    # def publishResource(self):
    #    pass
    #===========================================================================
            
################################################################

class TreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, icon = None, text = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element        
        text = text if text is not None else util.name(element)
        self.setText(0, text)        
        if icon is not None:
            self.setIcon(0, icon)            
            
    def refreshContent(self):
        self.takeChildren()
        self.populate()

    def parentCatalog(self):        
        item  = self            
        while item is not None:                    
            if isinstance(item, GsCatalogItem):
                return item.element                           
            item = item.parent()            
        return None              
    
class QgsLayerItem(TreeItem): 
    def __init__(self, layer ): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, layer, icon) 
     
class QgsGroupItem(TreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, group , icon)         

class QgsStyleItem(TreeItem): 
    def __init__(self, layer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeItem.__init__(self, layer, icon, "Style of layer '" + layer.name() + "'")         
            
class GsLayersItem(TreeItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, None, icon, "Layers") 
            
    def populate(self):
        layers = self.parentCatalog().get_layers()
        for layer in layers:
            layerItem = GsLayerItem(layer)            
            layerItem.populate()    
            self.addChild(layerItem)
                
class GsGroupsItem(TreeItem): 
    def __init__(self): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, None, icon, "Groups")   
        
    def populate(self):
        groups = self.parentCatalog().get_layergroups()
        for group in groups:
            groupItem = GsGroupItem(group)
            groupItem.populate()                                
            self.addChild(groupItem)         

class GsWorkspacesItem(TreeItem): 
    def __init__(self): 
        #icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, None, None, "Workspaces") 
    
    def populate(self):
        cat = self.parentCatalog()
        defaultWorkspace = cat.get_default_workspace()
        defaultWorkspace.fetch()
        defaultName = defaultWorkspace.dom.find('name').text             
        workspaces = cat.get_workspaces()
        for workspace in workspaces:
            workspaceItem = GsWorkspaceItem(workspace, workspace.name == defaultName)
            workspaceItem.populate()
            self.addChild(workspaceItem) 

class GsStylesItem(TreeItem): 
    def __init__(self ): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        TreeItem.__init__(self, None, icon, "Styles") 
                    
    def populate(self):
        styles = self.parentCatalog().get_styles()
        for style in styles:
            styleItem = GsStyleItem(style, False)                
            self.addChild(styleItem)
                
class GsCatalogItem(TreeItem): 
    def __init__(self, catalog, name): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/geoserver.png")
        TreeItem.__init__(self, catalog, icon, name) 
        
    def populate(self):
        #cat = self.element
        workspacesItem = GsWorkspacesItem()                              
        self.addChild(workspacesItem)  
        workspacesItem.populate()
        layersItem = GsLayersItem()                                      
        self.addChild(layersItem)
        layersItem.populate()
        groupsItem = GsGroupsItem()                                    
        self.addChild(groupsItem)
        groupsItem.populate()
        stylesItem = GsStylesItem()                        
        self.addChild(stylesItem)
        stylesItem.populate()      
                        
class GsLayerItem(TreeItem): 
    def __init__(self, layer): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        TreeItem.__init__(self, layer, icon)         
        
    def populate(self):
        layer = self.element
        for style in layer.styles:
            styleItem = GsStyleItem(style, False)
            self.addChild(styleItem)
        if layer.default_style is not None:
            styleItem = GsStyleItem(layer.default_style, True)                    
            self.addChild(styleItem)  
                

class GsGroupItem(TreeItem): 
    def __init__(self, group): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        TreeItem.__init__(self, group, icon)
        
    def populate(self):
        layers = self.element.catalog.get_layers()
        layersDict = {layer.name : layer for layer in layers}
        for layer in self.element.layers:
            layerItem = GsLayerItem(layersDict[layer])                    
            self.addChild(layerItem)
            #layerItem.populate()

class GsStyleItem(TreeItem): 
    def __init__(self, style, isDefault): 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        name = style.name if not isDefault else style.name + " [default style]"
        TreeItem.__init__(self, style, icon, name)
        self.isDefault = isDefault           
          
class GsWorkspaceItem(TreeItem): 
    def __init__(self, workspace, isDefault):                 
        self.isDefault = isDefault        
        name = workspace.name if not isDefault else workspace.name + " [default workspace]"
        TreeItem.__init__(self, workspace, None, name)  
        
    def populate(self):
        stores = self.element.catalog.get_stores(self.element)
        for store in stores:
            storeItem = GsStoreItem(store)
            storeItem.populate()
            self.addChild(storeItem)         
                             
class GsStoreItem(TreeItem): 
    def __init__(self, store):         
        TreeItem.__init__(self, store)

    def populate(self):
        resources = self.element.get_resources()
        for resource in resources:
            resourceItem = GsResourceItem(resource)                        
            self.addChild(resourceItem)        

class GsResourceItem(TreeItem): 
    def __init__(self, resource):         
        TreeItem.__init__(self, resource)
        

        
                 
