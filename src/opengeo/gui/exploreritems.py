from PyQt4 import QtGui
import os
from opengeo.core import util

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