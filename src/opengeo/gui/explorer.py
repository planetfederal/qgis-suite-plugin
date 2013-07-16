from PyQt4.QtCore import *
from PyQt4 import QtCore
from qgis.core import *
from opengeo.qgis import layers as qgislayers
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.catalogdialog import DefineCatalogDialog
from opengeo.gui.groupdialog import LayerGroupDialog
from opengeo.gui.workspacedialog import DefineWorkspaceDialog
from opengeo.gui.styledialog import StyleFromLayerDialog, AddStyleToLayerDialog,\
    PublishStyleDialog
from opengeo.gui.explorerthread import ExplorerThread
from opengeo.gui.layerdialog import PublishLayerDialog, PublishLayersDialog
from opengeo.gui.exploreritems import *
from opengeo.core.resource import Coverage, FeatureType
from opengeo.core.layer import Layer
from opengeo.core.style import Style


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
    
    def addGeoServerCatalog(self):         
        dlg = DefineCatalogDialog()
        dlg.exec_()
        cat = dlg.getCatalog()        
        if cat is not None:   
            name = dlg.getName()
            i = 2
            while name in self.catalogs.keys():
                name = dlg.getName() + "_" + str(i)
                i += 1                                 
            item = self.getGeoServerCatalogItem(cat, name)
            catalogsItem = self.tree.topLevelItem(0)
            catalogsItem.addChild(item)
            self.catalogs[name] = cat
        
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
        qgisItem.setText(0, "QGIS project") 
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
        styles = qgislayers.get_vector_layers()
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
        if isinstance(self.currentItem, (GsLayerItem, GsStyleItem, GsGroupItem, GsStoreItem)):                                    
            deleteLayersAction = QtGui.QAction("Delete", None)
            deleteLayersAction.triggered.connect(self.deleteElement)
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
        elif isinstance(self.currentItem, QgsStyleItem):                     
            publishStyleAction = QtGui.QAction("Publish...", None)
            publishStyleAction.triggered.connect(self.publishStyle)
            menu.addAction(publishStyleAction)                                            
        elif isinstance(self.currentItem, GsStylesItem):     
            createStyleFromLayerAction = QtGui.QAction("New style from QGIS layer...", None)
            createStyleFromLayerAction.triggered.connect(self.createStyleFromLayer)
            menu.addAction(createStyleFromLayerAction)                                                                            
        elif isinstance(self.currentItem, GsWorkspacesItem):                    
            createWorkspaceAction = QtGui.QAction("New workspace...", None)
            createWorkspaceAction.triggered.connect(self.createWorkspace)
            menu.addAction(createWorkspaceAction)                                                                     
        elif isinstance(self.currentItem, GsGroupsItem):    
            createGroupAction = QtGui.QAction("New group...", None)
            createGroupAction.triggered.connect(self.createGroup)
            menu.addAction(createGroupAction)                                                                        
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
                deleteLayerAction.triggered.connect(self.deleteElement)
                menu.addAction(deleteLayerAction)                                
                addLayerAction = QtGui.QAction("Add to current QGIS project", None)
                addLayerAction.triggered.connect(self.addLayerToProject)
                menu.addAction(addLayerAction)            
        elif isinstance(self.currentItem, GsGroupItem):    
            editLayerGroupAction = QtGui.QAction("Edit...", None)
            editLayerGroupAction.triggered.connect(self.editLayerGroup)
            menu.addAction(editLayerGroupAction)     
            deleteLayerGroupAction = QtGui.QAction("Delete", None)
            deleteLayerGroupAction.triggered.connect(self.deleteElement)
            menu.addAction(deleteLayerGroupAction)                                                                                                                                                      
        elif isinstance(self.currentItem, GsCatalogItem):                        
            removeCatalogAction = QtGui.QAction("Remove", None)
            removeCatalogAction.triggered.connect(self.removeCatalog)
            menu.addAction(removeCatalogAction)                                                                 
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
                deleteStyleAction.triggered.connect(self.deleteElement)
                menu.addAction(deleteStyleAction)            
        elif isinstance(self.currentItem, GsWorkspaceItem):                     
            setAsDefaultAction = QtGui.QAction("Set as default workspace", None)
            setAsDefaultAction.triggered.connect(self.setAsDefaultWorkspace)
            setAsDefaultAction.setEnabled(not self.currentItem.isDefault)
            menu.addAction(setAsDefaultAction)                                         
            deleteWorkspaceAction = QtGui.QAction("Delete", None)
            deleteWorkspaceAction.triggered.connect(self.deleteElement)
            menu.addAction(deleteWorkspaceAction)                                                            
        elif isinstance(self.currentItem, GsStoreItem):       
            deleteStoreAction = QtGui.QAction("Delete", None)
            deleteStoreAction.triggered.connect(self.deleteElement)
            menu.addAction(deleteStoreAction)                    
        elif isinstance(self.currentItem, GsResourceItem):        
            addResourceAsLayerAction = QtGui.QAction("Add to current QGIS project", None)
            addResourceAsLayerAction.triggered.connect(self.addResourceAsLayer)
            menu.addAction(addResourceAsLayerAction)                        
            deleteResourceAction = QtGui.QAction("Delete", None)
            deleteResourceAction.triggered.connect(self.deleteElement)
            menu.addAction(deleteResourceAction)                    
        
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
            if hasattr(value, 'element'):
                if hasattr(value.element, 'name') and hasattr(element, 'name'):
                    if  value.element.name == element.name and value.element.__class__ == element.__class__:
                        allItems.append(value)
                elif value.element == element:
                    allItems.append(value)                
            iterator += 1
            value = iterator.value()
        return allItems      
    
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
    
    def editLayerGroup(self):
        cat = self.currentItem.parentCatalog()        
        dlg = LayerGroupDialog(cat, self.currentItem.element)
        dlg.exec_()
        group = dlg.group
        if group is not None:
            self.run(cat.save, "Layer group '" + self.currentItem.element.name + "' correctly edited", group)   
    
        
            
    def addLayerToProject(self):
        cat = OGCatalog(self.currentItem.parentCatalog())                 
        self.run(cat.add_layer_to_project, 
                 "Layer '" + self.currentItem.element.name + "' correctly added to QGIS project", 
                 [],
                 self.currentItem.element.name)
        
    def deleteElement(self):        
        selected = self.tree.selectedItems()
        elements = []
        for item in selected:
            elements.append(item.element)
            if isinstance(item, GsStoreItem):
                for idx in range(item.childCount()):
                    subitem = item.child(idx)
                    elements.insert(0, subitem.element)        
        toUpdate = set(item.parent() for item in selected)                
        self.progress.setMaximum(len(elements))
        progress = 0        
        dependent = self.getDependentElements(elements)
        if dependent:
            msg = "The following elements depend on the elements to delete\nand will be deleted as well:\n\n"
            for e in dependent:
                msg += "-" + e.name + "(" + e.__class__.__name__ + ")\n\n"
            msg += "Do you really want to delete all these elements?"                   
            reply = QtGui.QMessageBox.question(self, "Delete confirmation",
                                               msg, QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
            toDelete = set()
            for e in dependent:                
                items = self.findAllItems(e);                
                toUpdate.update(set(item.parent() for item in items))
                toDelete.update(items)
            toUpdate = toUpdate - toDelete
        
        elements[0:0] = dependent        
        for element in elements:
            self.progress.setValue(progress)                                        
            self.run(element.catalog.delete,
                 element.__class__.__name__ + " '" + element.name + "' correctly deleted",
                 [], 
                 element)  
            progress += 1
        self.progress.setValue(progress)
        for item in toUpdate:
            item.refreshContent()
        self.progress.setValue(0)
        
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
        toPublish  = dlg.topublish
        if toPublish is None:
            return
        self.progress.setMaximum(len(toPublish))
        progress = 0        
        toUpdate = set();
        for layer, catalog, workspace in toPublish:
            self.progress.setValue(progress)            
            ogcat = OGCatalog(catalog)                 
            self.run(ogcat.publish_layer,
                     "Layer correctly published from layer '" + layer.name() + "'",
                     [],
                     layer, workspace, True)
            progress += 1
            toUpdate.add(self.findAllItems(catalog))
        self.progress.setValue(progress)
        
        for item in toUpdate:
            item.refreshContent()
        self.progress.setValue(0)
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
                 self.currentItem.element, True, dlg.name)
         
            
    def addResourceAsLayer(self):
        cat = OGCatalog(self.currentItem.parentCatalog())                 
        self.run(cat.add_layer_to_project, 
                 "Layer '" + self.currentItem.element.name + "' correctly added to QGIS project from resource", 
                 [self.currentItem.element],
                 self.currentItem.element.name)


        
                 
