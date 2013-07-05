import sys
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
from qgis.core import *
from opengeo.qgis import tools
from opengeo.qgis import layers as qgislayers
from opengeo.geoserver.workspace import Workspace
from opengeo.geoserver.layer import Layer


class GeoServerExplorer(QtGui.QDialog):
    
    def __init__(self, catalog = tools.defaultCatalog(), parent = None):
        super(GeoServerExplorer, self).__init__()
        self.catalog = catalog
        self.initGui()
        
    def initGui(self):      
        self.resize(400, 600) 
        self.setWindowTitle('GeoServer explorer')
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)                                    
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
    
    def fillTree(self):
        #Geoserver elements
        geoserverItem = QtGui.QTreeWidgetItem()
        geoserverItem.setText(0, "GeoServer catalog")
        workspacesItem = QtGui.QTreeWidgetItem()
        workspacesItem.setText(0, "Workspaces")
        workspaces = self.catalog.get_workspaces()
        for workspace in workspaces:
            workspaceItem = QtGui.QTreeWidgetItem()
            workspaceItem.setText(0, workspace.name)
            workspaceItem.setData(0, QtCore.Qt.UserRole, workspace)
            workspacesItem.addChild(workspaceItem)
            stores = self.catalog.get_stores(workspace)
            for store in stores:
                storeItem = QtGui.QTreeWidgetItem()
                storeItem.setText(0, store.name)
                storeItem.setData(0, QtCore.Qt.UserRole, store)
                workspaceItem.addChild(storeItem)
                resources = self.catalog.get_resources(store, workspace)
                for resource in resources:
                    resourceItem = QtGui.QTreeWidgetItem()
                    resourceItem.setText(0, resource.name)
                    resourceItem.setData(0, QtCore.Qt.UserRole, resource)
                    storeItem.addChild(resourceItem)
        geoserverItem.addChild(workspacesItem)  
        layersItem = QtGui.QTreeWidgetItem()
        layersItem.setText(0, "Layers")
        layers = self.catalog.get_layers()
        for layer in layers:
            layerItem = QtGui.QTreeWidgetItem()
            layerItem.setText(0, layer.name)
            layerItem.setData(0, QtCore.Qt.UserRole, layer)
            layersItem.addChild(layerItem)
        geoserverItem.addChild(layersItem)
        groupsItem = QtGui.QTreeWidgetItem()
        groupsItem.setText(0, "Groups")
        groups = self.catalog.get_layergroups()
        for group in groups:
            groupItem = QtGui.QTreeWidgetItem()
            groupItem.setText(0, group.name)
            groupItem.setData(0, QtCore.Qt.UserRole, group)
            for layer in group.layers:
                layerItem = QtGui.QTreeWidgetItem()
                layerItem.setText(0, layer)
                layerItem.setData(0, QtCore.Qt.UserRole, layer)
                groupItem.addChild(layerItem)
            groupsItem.addChild(groupItem)            
        geoserverItem.addChild(groupsItem)
        stylesItem = QtGui.QTreeWidgetItem()
        stylesItem.setText(0, "Styles")
        styles = self.catalog.get_styles()
        for style in styles:
            styleItem = QtGui.QTreeWidgetItem()
            styleItem.setText(0, style.name)
            styleItem.setData(0, QtCore.Qt.UserRole, style)
            stylesItem.addChild(styleItem)
        geoserverItem.addChild(stylesItem)
        self.tree.addTopLevelItem(geoserverItem)
        #QGis elements
        qgisItem = QtGui.QTreeWidgetItem()
        qgisItem.setText(0, "QGIS proyect")        
        layersItem = QtGui.QTreeWidgetItem()
        layersItem.setText(0, "Layers")
        layers = qgislayers.getAllLayers()
        for layer in layers:
            layerItem = QtGui.QTreeWidgetItem()
            layerItem.setText(0, layer.name())
            layerItem.setData(0, QtCore.Qt.UserRole, layer)
            layersItem.addChild(layerItem)
        qgisItem.addChild(layersItem)
        groupsItem = QtGui.QTreeWidgetItem()
        groupsItem.setText(0, "Groups")
        groups = qgislayers.getGroups()
        for group in groups:
            groupItem = QtGui.QTreeWidgetItem()
            groupItem.setText(0, group)
            groupItem.setData(0, QtCore.Qt.UserRole, group)            
            groupsItem.addChild(groupItem)
        qgisItem.addChild(groupsItem)
        stylesItem = QtGui.QTreeWidgetItem()
        stylesItem.setText(0, "Styles")
        styles = qgislayers.getAllLayers()
        for style in styles:
            styleItem = QtGui.QTreeWidgetItem()
            styleItem.setText(0, "style of layer '" + style.name() + "'")
            styleItem.setData(0, QtCore.Qt.UserRole, style)
            stylesItem.addChild(styleItem)
        qgisItem.addChild(stylesItem)
        self.tree.addTopLevelItem(qgisItem)
          
    
    def fillQgsTree(self):
        pass 
    
    #========== menus and actions =====================
     
            
    def showTreePopupMenu(self,point):
        currentItem = self.tree.itemAt(point)        
        self.currentElementData = currentItem.data(0, QtCore.Qt.UserRole)
        self.currentElementText = currentItem.text(0)
        popupmenu = QtGui.QMenu() 
        if isinstance(self.currentElementData, Workspace):                       
            setAsDefaultAction = QtGui.QAction("Set as default workspace...", self.tree)
            setAsDefaultAction.triggered.connect(self.setAsDefaultWorkspace)
            popupmenu.addAction(setAsDefaultAction)                                         
            popupmenu.exec_(self.tree.mapToGlobal(point))
        if isinstance(self.currentElementData, Layer):                       
            addLayerAction = QtGui.QAction("Add layer to current QGIS project", self.tree)
            addLayerAction.triggered.connect(self.addLayer)
            popupmenu.addAction(addLayerAction)                                         
            popupmenu.exec_(self.tree.mapToGlobal(point))            
        elif isinstance(self.currentElementData, QgsMapLayer): 
            if self.currentElementText.startswith("Style of layer"):
                publishStyleAction = QtGui.QAction("Publish style...", self.tree)
                publishStyleAction.triggered.connect(self.publishStyle)
                popupmenu.addAction(publishStyleAction)                                         
                popupmenu.exec_(self.tree.mapToGlobal(point)) 
            else:
                publishLayerAction = QtGui.QAction("Publish layer...", self.tree)
                publishLayerAction.triggered.connect(self.publishLayer)
                popupmenu.addAction(publishLayerAction)                                         
                popupmenu.exec_(self.tree.mapToGlobal(point))            

    def setAsDefaultWorkspace(self):
        pass
    
    def addLayer(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            tools.addLayerToProject(self.currentElementData.typename)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        #TODO:update tree
        
    def publishStyle(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            tools.publishStyle(self.currentElementData, self.catalog, True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        #TODO:update tree        
        
    def publishLayer(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor)) 
        try:
            tools.publishLayer(self.currentElementData, self.catalog, True)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        #TODO:update tree

