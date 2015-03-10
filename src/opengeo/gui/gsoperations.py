from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from qgis.core import *
from geoserver.layergroup import LayerGroup, UnsavedLayerGroup
from opengeo.qgis import layers as qgislayers
from opengeo.qgis.catalog import OGCatalog, createPGFeatureStore
from opengeo.gui.qgsexploreritems import QgsStyleItem
from opengeo.gui.gsnameutils import xmlNameEmptyRegex, xmlNameFixUp, \
    xmlNameRegex, xmlNameRegexMsg
from opengeo.qgis.utils import UserCanceledOperation
from opengeo.gui.dialogs.gsnamedialog import getGSLayerName
from opengeo.gui.dialogs.groupdialog import PublishLayerGroupDialog


def publishDraggedGroup(explorer, groupItem, catalog, workspace=None):
    groupname = groupItem.element
    groups = qgislayers.getGroups()
    grouplyrs = groups[groupname]

    overwrite = bool(QSettings().value(
        "/OpenGeo/Settings/GeoServer/OverwriteGroupLayers", True, bool))
    try:
        dlg = PublishLayerGroupDialog(catalog, groupname, grouplyrs,
                                      workspace=workspace,
                                      overwritegroup=True,
                                      overwritelayers=overwrite)
        dlg.exec_()
    except UserCanceledOperation:
        return False
    grpName = dlg.definedname
    toPublish = dlg.topublish
    if grpName is None:  # toPublish can be empty list
        return False
    catgroup = catalog.get_layergroup(grpName)

    names = []
    if toPublish:
        explorer.setProgressMaximum(len(toPublish), "Publish layers")
        progress = 0
        layernames = []
        for layer, catalog, workspc, layername in toPublish:
            layernames.append(layername)
            explorer.setProgress(progress)
            ogcat = OGCatalog(catalog)
            if not explorer.run(ogcat.publishLayer,
                                None,
                                [],
                                layer, workspc, True, layername):
                explorer.setProgress(0)
                return
            progress += 1
            explorer.setProgress(progress)
        explorer.resetActivity()
        names = reversed(layernames)

    if catgroup:
        catalog.delete(catgroup)

    #TODO calculate bounds
    bbox = None
    group = UnsavedLayerGroup(catalog, grpName, names, names, bbox)

    return explorer.run(catalog.save,
                        "Create layer group from group '" + groupname + "'",
                        [],
                        group)

def publishDraggedLayer(explorer, layer, workspace):
    cat = workspace.catalog
    ogcat = OGCatalog(cat)
    gslayers = [lyr.name for lyr in cat.get_layers()]
    try:
        lyrname = getGSLayerName(name=xmlNameFixUp(layer.name()),
                                 names=gslayers,
                                 unique=False)
    except UserCanceledOperation:
        return False

    return explorer.run(ogcat.publishLayer,
                        "Publish layer from layer '" + lyrname + "'",
                        [],
                        layer, workspace, True, lyrname)

def publishDraggedTable(explorer, table, workspace):    
    cat = workspace.catalog                          
    return explorer.run(publishTable,
             "Publish table from table '" + table.name + "'",
             [],
             table, cat, workspace)
    
            
def publishTable(table, catalog = None, workspace = None):
    if catalog is None:
        pass       
    workspace = workspace if workspace is not None else catalog.get_default_workspace()
    connection = table.conn   
    geodb = connection.geodb     
    store = createPGFeatureStore(catalog,
                         connection.name,
                         workspace = workspace,
                         overwrite = True,
                         host = geodb.host,
                         database = geodb.dbname,
                         schema = table.schema,
                         port = geodb.port,
                         user = geodb.user,
                         passwd = geodb.passwd)
    if store is not None:
        catalog.publish_featuretype(table.name, store, "EPSG:" + str(table.srid))

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
