from PyQt4.QtCore import *
from qgis.core import *
from opengeo.gui.gsexploreritems import *
from opengeo.gui.qgsexploreritems import *
from opengeo.geoserver import utils as gsutils
from opengeo.postgis import postgis_utils as pgutils


class ExplorerTreeWidget(QtGui.QTreeWidget):
   
    def __init__(self, explorer):         
        self.explorer = explorer
        QtGui.QTreeWidget.__init__(self, None) 
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)                    
        self.setColumnCount(1)            
        self.header().hide()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showTreePopupMenu)
        self.itemClicked.connect(self.treeItemClicked) 
        self.setDragDropMode(QtGui.QTreeWidget.DragDrop)                
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.catalogs = {}
        self.qgisItem = None
        self.lastClicked = None
  
    def refreshContent(self):
        pass        
        #self.qgisItem.refreshContent()      
        
    def getSelectionTypes(self):
        items = self.selectedItems()
        return set([type(item) for item in items])  
        
    def treeItemClicked(self, item, column): 
        self.lastClicked = item
        if hasattr(item, 'descriptionWidget'):
            widget = item.descriptionWidget(self, self.explorer)
            if widget is not None:
                self.explorer.setDescriptionWidget(widget) 
        allTypes = self.getSelectionTypes()                
        if len(allTypes) != 1:
            return 
        items = self.selectedItems()
        if len(items) == 1:
            actions = item.contextMenuActions(self, self.explorer)
            if (isinstance(item, TreeItem) and hasattr(item, 'populate')):            
                refreshAction = QtGui.QAction("Refresh", self.explorer)
                refreshAction.triggered.connect(item.refreshContent)
                actions.append(refreshAction) 
            self.explorer.setToolbarActions(actions)
    
    def lastClickedItem(self):
        return self.lastClicked
    
    def showTreePopupMenu(self,point):
        allTypes = self.getSelectionTypes()                
        if len(allTypes) != 1:
            return 
        items = self.selectedItems()
        if len(items) > 1:
            self.showMultipleSelectionPopupMenu(point)
        else:
            self.showSingleSelectionPopupMenu(point)
                
    def getDefaultWorkspace(self, catalog):                            
        workspaces = catalog.get_workspaces()
        if workspaces:
            return catalog.get_default_workspace()
        else:
            return None
                        
    def showMultipleSelectionPopupMenu(self, point):        
        self.selectedItem = self.itemAt(point)  
        point = self.mapToGlobal(point)        
        menu = QtGui.QMenu()
        actions = self.selectedItem.multipleSelectionContextMenuActions(self, self.explorer, self.selectedItems())
        for action in actions:
            menu.addAction(action)            
        menu.exec_(point)             
                                            
                
    def showSingleSelectionPopupMenu(self, point):                
        self.selectedItem = self.itemAt(point)
        if not isinstance(self.selectedItem, TreeItem):
            return                  
        menu = QtGui.QMenu()
        if (isinstance(self.selectedItem, TreeItem) and hasattr(self.selectedItem, 'populate')):            
            refreshAction = QtGui.QAction("Refresh", None)
            refreshAction.triggered.connect(self.selectedItem.refreshContent)
            menu.addAction(refreshAction) 
        point = self.mapToGlobal(point)    
        actions = self.selectedItem.contextMenuActions(self, self.explorer)
        for action in actions:
            menu.addAction(action)            
        menu.exec_(point)

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
        if not allItems:
            allItems = [None] #Signal that the whole tree has to be updated
        return allItems      
    

                    
###################################DRAG & DROP########################    
    
    QGIS_URI_MIME = "application/x-vnd.qgis.qgis.uri"
 
    def mimeTypes(self):
        return ["application/x-qabstractitemmodeldatalist", self.QGIS_URI_MIME]
     
    def mimeData(self, items):        
        mimeData = QtGui.QTreeWidget.mimeData(self, items)               
        encodedData = QByteArray()
        stream = QDataStream(encodedData, QIODevice.WriteOnly)
  
        for item in items:
            if isinstance(item, GsLayerItem):                
                layer = item.element
                uri = gsutils.mimeUri(layer)                                
                stream.writeQString(uri)
            elif isinstance(item, PgTableItem):
                table = item.element
                uri = pgutils.mimeUri(table)                          
                stream.writeQString(uri)                
  
        mimeData.setData(self.QGIS_URI_MIME, encodedData)        
        return mimeData
        
    def dropEvent(self, event):
        if isinstance(event.source(), ExplorerTreeWidget):
            self.dropExplorerItemEvent(event)
        else:
            destinationItem=self.itemAt(event.pos())        
            mimeData = event.mimeData()
            elements = []            
            for mimeFormat in mimeData.formats():                
                if mimeFormat != self.QGIS_URI_MIME:
                    continue            
                encoded = mimeData.data(mimeFormat)
                stream = QtCore.QDataStream(encoded, QtCore.QIODevice.ReadOnly)
                while not stream.atEnd():
                    mimeUri = stream.readQString()
                    elements.append(mimeUri)            
            if elements:
                destinationItem.startDropEvent()
                self.explorer.progress.setMaximum(len(elements))
                toUpdate = set()
                for i, element in enumerate(elements):
                    destinationItem.acceptDroppedUri(self.explorer, element)                                                                            
                    self.explorer.progress.setValue(i)                
                toUpdate = destinationItem.finishDropEvent(self.explorer)
                for item in toUpdate:
                    item.refreshContent()        
                self.explorer.resetActivity()
                event.acceptProposedAction()    
 
    
    def dropExplorerItemEvent(self, event):        
        destinationItem=self.itemAt(event.pos())
        draggedTypes = {item.__class__ for item in event.source().selectedItems()}
        if len(draggedTypes) > 1:
            return            
        
        selected = self.selectedItems()
        self.explorer.progress.setMaximum(len(selected))
        i = 0
        toUpdate = set()
        for item in selected:
            updatable = destinationItem.acceptDroppedItem(self, self.explorer, item)
            if updatable is not None:  
                toUpdate.update(updatable)                                      
            i += 1
            self.explorer.progress.setValue(i)
        
        for item in toUpdate:
            item.refreshContent()        
        self.explorer.progress.setValue(0)
        event.acceptProposedAction()
        
        

        
     
                    
        
        

        
                    
            



                 
