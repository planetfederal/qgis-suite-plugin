import os
from PyQt4 import QtGui, QtCore
from opengeo.gui.gsexploreritems import GsCatalogsItem, \
    GsLayerItem, GsWorkspaceItem, GsStyleItem, GsGroupItem,\
    GwcLayerItem, GsProcessItem
from opengeo.qgis import layers as qgislayers
from opengeo.gui.explorertree import ExplorerTreeWidget
from opengeo.geoserver.gwc import Gwc
from opengeo.postgis.connection import PgConnection
from opengeo.gui.pgexploreritems import PgConnectionsItem, PgSchemaItem
from opengeo.gui.qgsexploreritems import QgsProjectItem, QgsGroupItem,\
    QgsLayerItem, QgsStyleItem
from opengeo.geoserver.wps import Wps

class GsTreePanel(QtGui.QWidget):
    
    def __init__(self, explorer):                 
        QtGui.QWidget.__init__(self, None) 
        self.explorer = explorer
        self.catalogsItem = GsCatalogsItem()                    
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(2)
        verticalLayout.setMargin(0)      
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(2)
        horizontalLayout.setMargin(0)    
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.comboBox.currentIndexChanged.connect(self.catalogHasChanged)   
        horizontalLayout.addWidget(self.comboBox)
        self.addButton = QtGui.QPushButton()
        self.addButton.clicked.connect(self.addCatalog)
        addIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
        self.addButton.setIcon(addIcon)
        self.addButton.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum) 
        self.refreshButton = QtGui.QPushButton()
        self.refreshButton.clicked.connect(self.refreshContent)
        refreshIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/refresh.png")
        self.refreshButton.setIcon(refreshIcon)
        self.refreshButton.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum) 
        self.refreshButton.setEnabled(False)
        horizontalLayout.addWidget(self.refreshButton)
        horizontalLayout.addWidget(self.addButton)        
        verticalLayout.addLayout(horizontalLayout)
        self.toptoolbar = QtGui.QToolBar()
        self.toptoolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toptoolbar.setVisible(False)
        verticalLayout.addWidget(self.toptoolbar)
        self.tree = ExplorerTreeWidget(self.explorer)        
        verticalLayout.addWidget(self.tree)        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        layersIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        self.layersAction = QtGui.QAction(layersIcon, "Layers", explorer)
        self.layersAction.triggered.connect(lambda: self.toggleVisibility((GsLayerItem), 
                                            self.catalogItem.child(1).contextMenuActions(self.tree, self.explorer)))        
        workspacesIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/workspace.png")
        self.workspacesAction = QtGui.QAction(workspacesIcon, "Workspaces", explorer)
        self.workspacesAction.triggered.connect(lambda: self.toggleVisibility((GsWorkspaceItem),
                                                self.catalogItem.child(0).contextMenuActions(self.tree, self.explorer))) 
        stylesIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        self.stylesAction = QtGui.QAction(stylesIcon, "Styles", explorer)
        self.stylesAction.triggered.connect(lambda: self.toggleVisibility((GsStyleItem),
                                            self.catalogItem.child(3).contextMenuActions(self.tree, self.explorer))) 
        groupsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        self.groupsAction = QtGui.QAction(groupsIcon, "Groups", explorer)
        self.groupsAction.triggered.connect(lambda: self.toggleVisibility((GsGroupItem),
                                            self.catalogItem.child(2).contextMenuActions(self.tree, self.explorer))) 
        gwcIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/gwc.png")
        self.gwcAction = QtGui.QAction(gwcIcon, "GeoWebCache", explorer)
        self.gwcAction.triggered.connect(lambda: self.toggleVisibility((GwcLayerItem),
                                        self.catalogItem.child(4).contextMenuActions(self.tree, self.explorer))) 
        wpsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/process.png")
        self.wpsAction = QtGui.QAction(wpsIcon, "Processes", explorer)
        self.wpsAction.triggered.connect(lambda: self.toggleVisibility((GsProcessItem),
                                        self.catalogItem.child(5).contextMenuActions(self.tree, self.explorer))) 
        self.layersAction.setEnabled(False)
        self.workspacesAction.setEnabled(False)
        self.stylesAction.setEnabled(False)
        self.groupsAction.setEnabled(False)
        self.gwcAction.setEnabled(False)
        self.wpsAction.setEnabled(False)
        self.toolbar.addAction(self.layersAction)
        self.toolbar.addAction(self.workspacesAction)
        self.toolbar.addAction(self.stylesAction)
        self.toolbar.addAction(self.groupsAction)
        self.toolbar.addAction(self.gwcAction)
        self.toolbar.addAction(self.wpsAction)
        verticalLayout.addWidget(self.toolbar)
        self.setLayout(verticalLayout)                
    
    def catalogHasChanged(self):
        self.catalog = self.comboBox.itemData(self.comboBox.currentIndex())
        self.fillTree()
        self.toggleVisibility((GsLayerItem))
            
    def currentItem(self):
        self.tree.currentItem()
    
    def fillTree(self):    
        self.tree.clear() 
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor)) 
        self.explorer.progress.setMaximum(6)      
        try:
            groups = self.catalog.get_layergroups()
            for group in groups:
                groupItem = GsGroupItem(group)
                groupItem.populate()                                
                self.tree.addTopLevelItem(groupItem)          
            self.explorer.progress.setValue(1)
            cat = self.catalog            
            try:
                defaultWorkspace = cat.get_default_workspace()
                defaultWorkspace.fetch()
                defaultName = defaultWorkspace.dom.find('name').text
            except:
                defaultName = None             
            self.explorer.progress.setValue(2)
            workspaces = cat.get_workspaces()
            for workspace in workspaces:
                workspaceItem = GsWorkspaceItem(workspace, workspace.name == defaultName)
                workspaceItem.populate()
                self.tree.addTopLevelItem(workspaceItem)
            self.explorer.progress.setValue(3)
            styles = self.catalog.get_styles()
            for style in styles:
                styleItem = GsStyleItem(style, False)                
                self.tree.addTopLevelItem(styleItem)
            self.explorer.progress.setValue(4)                    
            layers = self.catalog.get_layers()
            for layer in layers:
                layerItem = GsLayerItem(layer)            
                layerItem.populate()    
                self.tree.addTopLevelItem(layerItem)
            self.explorer.progress.setValue(5)                   
            gwc = Gwc(self.catalog)        
            layers = gwc.layers()
            for layer in layers:
                item = GwcLayerItem(layer)
                self.tree.addTopLevelItem(item)
            self.explorer.progress.setValue(6)
            self.element = Wps(self.catalog)        
            processes = self.element.processes()
            for process in processes:
                item = GsProcessItem(process)
                self.tree.addTopLevelItem(item)                
        finally:
            self.explorer.progress.setValue(0)
            QtGui.QApplication.restoreOverrideCursor()

    def toggleVisibility(self, visibleItems = (type(None)), visibleActions = []):
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            item.setHidden(not isinstance(item, visibleItems))
        self.toptoolbar.setVisible(len(visibleActions)>0)
        self.toptoolbar.clear()
        for action in visibleActions:
            self.toptoolbar.addAction(action)
        self.visibleItems = visibleItems
        self.visibleActions = visibleActions
    
    def addCatalog(self):
        count = self.catalogsItem.childCount()
        self.catalogsItem.addGeoServerCatalog(self.explorer)
        newCount = self.catalogsItem.childCount()
        if newCount > count:
            self.catalogItem = self.catalogsItem.child(count)     
            self.catalog = self.catalogItem.element       
            self.comboBox.addItem(self.catalogItem.text(0), self.catalog)            
            self.layersAction.setEnabled(True)
            self.workspacesAction.setEnabled(True)
            self.stylesAction.setEnabled(True)
            self.groupsAction.setEnabled(True)
            self.gwcAction.setEnabled(True)
            self.wpsAction.setEnabled(True)
            self.refreshButton.setEnabled(True)
            self.fillTree()
            self.layersAction.trigger()   
    
    def catalogs(self):
        catalogs = {}
        for i in range(self.catalogsItem.childCount()):
            item = self.catalogsItem.child(i)
            catalogs[item.text(0)] = item.element
        return catalogs
            
    def refreshContent(self):
        self.fillTree()   
        self.toggleVisibility(self.visibleItems, self.visibleActions)                           


class PgTreePanel(QtGui.QWidget):
            
    def __init__(self, explorer):                 
        QtGui.QWidget.__init__(self, None) 
        self.explorer = explorer
        self.connectionsItem = PgConnectionsItem()
        self.connection = None                
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(2)
        verticalLayout.setMargin(0)      
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(2)
        horizontalLayout.setMargin(0)    
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum) 
        self.comboBox.currentIndexChanged.connect(self.connectionHasChanged)    
        horizontalLayout.addWidget(self.comboBox)
        self.addButton = QtGui.QPushButton()
        self.addButton.clicked.connect(self.addConnection)
        addIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
        self.addButton.setIcon(addIcon)
        self.addButton.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum) 
        self.refreshButton = QtGui.QPushButton()
        self.refreshButton.clicked.connect(self.refreshContent)
        refreshIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/refresh.png")
        self.refreshButton.setIcon(refreshIcon)
        self.refreshButton.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addWidget(self.refreshButton) 
        horizontalLayout.addWidget(self.addButton)
        verticalLayout.addLayout(horizontalLayout)        
        self.tree = ExplorerTreeWidget(self.explorer)        
        verticalLayout.addWidget(self.tree)                
        self.setLayout(verticalLayout)   
        self.populateComboBox()
        self.refreshContent()     
    
    def populateComboBox(self):
        connections = []
        settings = QtCore.QSettings()
        settings.beginGroup(u'/PostgreSQL/connections')
        for name in settings.childGroups():
            settings.beginGroup(name)
            try:                                            
                conn = PgConnection(name, settings.value('host'), int(settings.value('port')), 
                                settings.value('database'), settings.value('username'), 
                                settings.value('password'))                 
                connections.append(conn)                
            except Exception, e:                
                pass
            finally:                            
                settings.endGroup() 
        for conn in connections:
            self.comboBox.addItem(conn.name, conn)
        if connections:
            self.connection = connections[0]
    
    def addConnection(self):
        pass
    
    def connectionHasChanged(self):
        print str(self.comboBox.currentIndex())
        self.connection = self.comboBox.itemData(self.comboBox.currentIndex())        
        self.refreshContent()
        
    def refreshContent(self):
        if self.connection is None:
            return
        self.tree.clear()        
        schemas = self.connection.schemas()
        for schema in schemas:
            schemItem = PgSchemaItem(schema)
            schemItem.populate()
            self.tree.addTopLevelItem(schemItem)
         
        
    def currentItem(self):
        self.tree.currentItem()        
                        
class QgsTreePanel(QtGui.QWidget):    
    
    def __init__(self, explorer):                 
        QtGui.QWidget.__init__(self, None) 
        self.explorer = explorer
        self.projectItem = QgsProjectItem()                    
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(2)
        verticalLayout.setMargin(0)              
        self.tree = ExplorerTreeWidget(self.explorer)        
        verticalLayout.addWidget(self.tree)        
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        layersIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")
        self.layersAction = QtGui.QAction(layersIcon, "Layers", explorer)
        self.layersAction.triggered.connect(self.showLayers)                
        stylesIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/style.png")
        self.stylesAction = QtGui.QAction(stylesIcon, "Styles", explorer)
        self.stylesAction.triggered.connect(self.showStyles)
        groupsIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/group.gif")
        self.groupsAction = QtGui.QAction(groupsIcon, "Groups", explorer)
        self.groupsAction.triggered.connect(self.showGroups)                
        self.toolbar.addAction(self.layersAction)        
        self.toolbar.addAction(self.stylesAction)
        self.toolbar.addAction(self.groupsAction)        
        verticalLayout.addWidget(self.toolbar)
        self.setLayout(verticalLayout)
        self.lastAction = None
        self.layersAction.trigger()
                
    def currentItem(self):
        self.tree.currentItem()
    
    def showGroups(self):  
        if self.sender() == self.lastAction:
            return      
        self.tree.clear()     
        groups = qgislayers.getGroups()
        for group in groups:
            groupItem = QgsGroupItem(group)                                
            groupItem.populate()
            self.tree.addTopLevelItem(groupItem)          
        self.lastAction = self.sender()
            
    def showStyles(self):
        if self.sender() == self.lastAction:
            return
        self.tree.clear()
        styles = qgislayers.getVectorLayers()
        for style in styles:
            styleItem = QgsStyleItem(style)               
            self.tree.addTopLevelItem(styleItem)
        self.lastAction = self.sender()
                     
    def showLayers(self):              
        if self.sender() == self.lastAction:
            return           
        self.tree.clear()
        layers = qgislayers.getAllLayers()
        for layer in layers:
            layerItem = QgsLayerItem(layer)                                    
            self.tree.addTopLevelItem(layerItem)
        self.lastAction = self.sender()                                   
            
    def refreshContent(self):
        action = self.lastAction
        self.lastAction = None
        if action is not None:
            action.trigger()  
                                

                 
        
        