from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from qgis.core import *            
from opengeo.qgis import layers
from opengeo.qgis.catalog import OGCatalog
from opengeo.gui.overwrite import publishLayer
            
def publishDraggedGroup(explorer, groupItem, catalog, workspace):        
    groupName = groupItem.element
    groups = layers.getGroups()   
    group = groups[groupName]           
    gslayers= [layer.name for layer in catalog.get_layers()]
    missing = []         
    overwrite = bool(QSettings().value("/OpenGeo/Settings/GeoServer/OverwriteGroupLayers", True, bool)) 
    for layer in group:            
        if layer.name() not in gslayers or overwrite:
            missing.append(layer)         
    if missing:
        explorer.setProgressMaximum(len(missing), "Publish layers")
        progress = 0
        ogcat = OGCatalog(catalog)                  
        for layer in missing:
            explorer.setProgress(progress)                                           
            explorer.run(ogcat.publishLayer,
                     None,
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
    ret = explorer.run(publishLayer,
             "Publish layer from layer '" + layer.name() + "'",
             [],
             ogcat, layer, workspace, True)    
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
                    explorer.setError("Error reading file {} or it is not a valid layer file".format(name))
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
