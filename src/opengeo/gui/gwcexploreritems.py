from PyQt4 import QtGui,QtCore
from opengeo.gui.dialogs.gwclayer import EditGwcLayerDialog, SeedGwcLayerDialog
from opengeo.geoserver.gwc import Gwc, GwcLayer, SeedingStatusParsingError
from geoserver.catalog import FailedRequestError
from opengeo.gui.exploreritems import TreeItem
import os
from opengeo.gui.confirm import confirmDelete

class GwcTreeItem(TreeItem):
    
    def iconPath(self):
        return os.path.dirname(__file__) + "/../images/gwc.png"
                                             
class GwcLayersItem(GwcTreeItem): 
    def __init__(self, catalog):
        self.catalog = catalog
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/gwc.png")
        TreeItem.__init__(self, None, icon, "GeoWebCache layers")                                    
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)

    def populate(self):
        catalog = self.catalog
        self.element = Gwc(catalog)        
        layers = self.element.layers()
        for layer in layers:
            item = GwcLayerItem(layer)
            self.addChild(item)

    def acceptDroppedItem(self, tree, explorer, item):  
        from opengeo.gui.gsexploreritems import GsLayerItem
        if isinstance(item, GsLayerItem):      
            if createGwcLayer(explorer, item.element):
                return [self]
        else:
            return []
    
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/add.png")
        addGwcLayerAction = QtGui.QAction(icon, "New GWC layer...", explorer)
        addGwcLayerAction.triggered.connect(lambda: self.addGwcLayer(tree, explorer))
        return [addGwcLayerAction]        
               
     
    def addGwcLayer(self, tree, explorer):
        cat = self.catalog
        layers = cat.get_layers()              
        dlg = EditGwcLayerDialog(layers, None)
        dlg.exec_()        
        if dlg.gridsets is not None:
            layer = dlg.layer
            gwc = Gwc(layer.catalog)
            
            #TODO: this is a hack that assumes the layer belongs to the same workspace
            typename = layer.resource.workspace.name + ":" + layer.name
            
            gwclayer = GwcLayer(gwc, typename, dlg.formats, dlg.gridsets, dlg.metaWidth, dlg.metaHeight)
            catItem = tree.findAllItems(cat)[0]            
            explorer.run(gwc.addLayer,
                              "Create GWC layer '" + layer.name + "'",
                              [catItem.gwcItem],
                              gwclayer)             
                            

          
                
class GwcLayerItem(GwcTreeItem): 
    def __init__(self, layer):          
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer.png")        
        TreeItem.__init__(self, layer, icon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)
        
    def contextMenuActions(self, tree, explorer):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/edit.png")
        editGwcLayerAction = QtGui.QAction(icon, "Edit...", explorer)
        editGwcLayerAction.triggered.connect(lambda: self.editGwcLayer(explorer))
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/seed.png")          
        seedGwcLayerAction = QtGui.QAction(icon, "Seed...", explorer)
        seedGwcLayerAction.triggered.connect(lambda: self.seedGwcLayer(explorer))        
        emptyGwcLayerAction = QtGui.QAction("Empty", explorer)
        emptyGwcLayerAction.triggered.connect(lambda: self.emptyGwcLayer(explorer)) 
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")                         
        deleteLayerAction = QtGui.QAction(icon, "Delete", explorer)
        deleteLayerAction.triggered.connect(lambda: self.deleteLayer(explorer))
        return[editGwcLayerAction, seedGwcLayerAction, emptyGwcLayerAction, deleteLayerAction]

    def acceptDroppedItem(self, tree, explorer, item): 
        from opengeo.gui.gsexploreritems import GsLayerItem 
        if isinstance(item, GsLayerItem):      
            if createGwcLayer(explorer, item.element):
                return [self.parent()]
        else:
            return []
        
    def multipleSelectionContextMenuActions(self, tree, explorer, selected):
        icon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/delete.gif")
        deleteSelectedAction = QtGui.QAction(icon, "Delete", explorer)
        deleteSelectedAction.triggered.connect(lambda: self.deleteLayers(explorer, selected))
        return [deleteSelectedAction]
    

    def _getDescriptionHtml(self, tree, explorer):                                
        html = '<p><b>Seeding status</b></p>'     
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
        try:
            text = self.getDescriptionHtml(tree, explorer)
            self.description.setHtml(text)
        except:
            explorer.setDescriptionWidget()
        
          
    def deleteLayer(self, explorer):
        self.deleteLayers(explorer, [self])      
        
    def deleteLayers(self, explorer, items):
        if not confirmDelete():
            return
        explorer.setProgressMaximum(len(items), "Deleting GWC layers")
        toUpdate = set()
        for i, item in enumerate(items):                    
            explorer.run(item.element.delete,
                     None,
                     [])             
            explorer.setProgress(i)
            toUpdate.add(item.parent())         
        for item in toUpdate:
            if item is not None:
                item.refreshContent(explorer)
        if None in toUpdate:
            explorer.refreshContent()
        explorer.resetActivity()
        explorer.setDescriptionWidget()            
              
        
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
            
            
         
        
def createGwcLayer(explorer, layer):                
    dlg = EditGwcLayerDialog([layer], None)
    dlg.exec_()        
    if dlg.gridsets is not None:
        gwc = Gwc(layer.catalog)
        
        #TODO: this is a hack that assumes the layer belongs to the same workspace
        typename = layer.resource.workspace.name + ":" + layer.name
        
        gwclayer = GwcLayer(gwc, typename, dlg.formats, dlg.gridsets, dlg.metaWidth, dlg.metaHeight)
        explorer.run(gwc.addLayer,
                          "Create GWC layer '" + layer.name + "'",
                          [],
                          gwclayer)  
        return True
    else:
        return False                 
            