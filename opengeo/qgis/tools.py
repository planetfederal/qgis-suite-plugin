# -*- coding: utf-8 -*-

'''
Main functions for plugin functionality.
This is supposed to contain the functions to be called when using plugin 
functionality from the QGIS console
'''

import os
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from opengeo.qgis import layers, exporter
from opengeo.geoserver.catalog import ConflictingDataError, UploadError
from opengeo.geoserver.catalog import Catalog
import opengeo.config
import urllib
from xml.dom import minidom


def defaultCatalog():
    return Catalog("http://localhost:8080/geoserver/rest")

def publishStyle(layer, catalog=defaultCatalog(), overwrite = False):
 
    '''
    Publishes the style of a given layer style in the specified catalog. If the overwrite parameter is True, 
    it will overwrite a style with that name in case it exists
    '''
    
    if isinstance(layer, basestring):
        layer = layers.resolveLayer(layer)         
    sld = getStyleAsSLD(layer)
    print sld    
    catalog.create_style(layer.name(), sld, overwrite)
    
    

def publishProject():
    pass
   
def getStyleAsSLD(layer):
    
    document = QDomDocument()
    header = document.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"UTF-8\"" )
    document.appendChild( header )
        
    root = document.createElementNS( "http://www.opengis.net/sld", "StyledLayerDescriptor" )
    root.setAttribute( "version", "1.1.0" )
    root.setAttribute( "xsi:schemaLocation", "http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" )
    root.setAttribute( "xmlns:ogc", "http://www.opengis.net/ogc" )
    root.setAttribute( "xmlns:se", "http://www.opengis.net/se" )
    root.setAttribute( "xmlns:xlink", "http://www.w3.org/1999/xlink" )
    root.setAttribute( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance" )
    document.appendChild( root )

    namedLayerNode = document.createElement( "NamedLayer" )
    root.appendChild( namedLayerNode )
            
    errorMsg = ""
            
    layer.writeSld(namedLayerNode, document, errorMsg)
    
    return unicode(document.toString(4))


def getDataFromLayer(layer):
    '''
    Returns the data corresponding to a given layer, ready to be passed to the
    method in the Catalog class for uploading to GeoServer.
    If needed, it performs and export to ensure that the file format is supported 
    by the GeoServer REST API to be used for import. In that case, the data returned
    will point to the exported copy of the data, not the original data source
    '''
    if layer.type() == layer.RasterLayer:
        data = exporter.exportRasterLayer(layer)                              
    else:      
        filename = exporter.exportVectorLayer(layer)        
        basename, extension = os.path.splitext(filename)        
        data = {
            'shp': basename + '.shp',
            'shx': basename + '.shx',
            'dbf': basename + '.dbf',
            'prj': basename + '.prj'
        }
    return data


def createStore(layer, catalog=defaultCatalog(), workspace=None, overwrite=False, title=None,
                       abstract=None, permissions=None, keywords=()):
    
    '''Creates a datastore for the specified layer'''
    
    if isinstance(layer, basestring):
        layer = layers.resolveLayer(layer)     
    #name = layer.name() if name is None else name

    if layer.type() == layer.RasterLayer:
        create_store_and_resource= catalog.create_coveragestore      
    elif layer.type() == layer.VectorLayer:
        create_store_and_resource= catalog.create_featurestore
    else:
        msg = layer.name() + ' is not a valid raster or vector layer'
        raise Exception(msg)

    #convert to a format that can be used for publication, if needed    
    data = getDataFromLayer(layer)
    
    #TODO: validation of the name
    #TODO: in case the name already exist, prompt user to ask for overwrite
    #TODO: manage PostGIS datastore type


    try:
        create_store_and_resource(layer.name(),
                                   data,
                                   workspace=workspace,
                                   overwrite=overwrite)
    except UploadError, e:
        msg = ('Could not save the layer %s, there was an upload '
               'error: %s' % (layer.name(), str(e)))
        e.args = (msg,)
        raise
    except ConflictingDataError, e:
        # A datastore of this name already exists
        msg = ('GeoServer reported a conflict creating a store with name %s: '
               '"%s". This should never happen because a brand new name '
               'should have been generated. But since it happened, '
               'try renaming the file or deleting the store in '
               'GeoServer.' % (layer.name(), str(e)))
        e.args = (msg,)
        raise


    # Verify the resource was created
    gs_resource = catalog.get_resource(layer.name())
    if gs_resource is not None:
        assert gs_resource.name == layer.name()
    else:
        msg = ('could not create layer %s.' % layer.name())
        raise Exception(msg)
   
    if gs_resource.latlon_bbox is None:
        box = gs_resource.native_bbox[:4]
        minx, maxx, miny, maxy = [float(a) for a in box]
        if -180 <= minx <= 180 and -180 <= maxx <= 180 and \
                -90 <= miny <= 90 and -90 <= maxy <= 90:
            gs_resource.latlon_bbox = gs_resource.native_bbox
            gs_resource.projection = "EPSG:4326"
            catalog.save(gs_resource)
        else:
            msg = ('GeoServer failed to detect the projection for layer '
                   '[%s]. It doesn\'t look like EPSG:4326, so backing out '
                   'the layer.')
            raise Exception(msg % layer.name())
        
def publishGroup(name, catalog=defaultCatalog(), workspace=None, overwrite=False, overwriteLayers = False):
    
    ''' 
    Publishes a group in the given catalog
    
    name: the name of the QGIS group to publish. It will also be used as the GeoServer layergroup name
    
    catalog:The catalog to publish to
    
    workspace: The workspace to add the group to
    
    overwrite: if True, it will overwrite a previous group with the specified name, if it exists
    
    overwriteLayers: if False, in case a layer in the group is not found in the specified workspace, the corresponding layer
    from the current QGIS project will be published, but all layers of the group that can be found in the GeoServer
    workspace will not be published. If True, all layers in the group are published, even if layers with the same name 
    exist in the workspace
    '''
    
    groups = layers.getGroups()
    if name not in groups:
        raise Exception("the specified group does not exist")
    
    group = groups[name]
    
    for layer in group:
        layer = catalog.get_layer(layer)
        if layer is None:
            publishLayer(layer, catalog, workspace, None, overwrite)
            
    layergroup = catalog.create_layergroup(name, group, group)
    catalog.save(layergroup)
    
def publishLayer (layer, catalog=defaultCatalog(), workspace=None, overwrite=False, title=None,
                       abstract=None, permissions=None, keywords=()):
    '''
    Publishes a QGIS layer. 
    It creates the corresponding store and the layer itself 
    If the layer is a group layer, it publishes all the layers individually and then creates 
    the layer group in the server
    
    layer: the layer to publish, whether as a QgsMapLayer object or its name in the QGIS TOC.
        
    catalog. A catalog object with information about the URL of the service to publish to.
    
    workspace: the workspace to publish to. USes the default project if not passed 
    or None 
    
    name: the name for the published layer. Uses the QGIS layer name if not passed 
    or None
       
    params: a dict with additional configuration parameters if needed
    
    '''
    
    if isinstance(layer, basestring):
        layer = layers.resolveLayer(layer)          
      
    if layer.type() == layer.VectorLayer:  
        #publish style
        publishStyle(layer, catalog)
    
    #create store
    createStore(layer, catalog)      

    if layer.type() == layer.VectorLayer:
        #assign style to created store  
        publishing = catalog.get_layer(layer.name())        
        #FIXME: Should we use the fully qualified typename?
        publishing.default_style = catalog.get_style(layer.name())
        catalog.save(publishing)
        
def addLayerToProject(typename, catalog = defaultCatalog()):
    '''
    Adds a new layer to the current project based on a layer in a GeoServer catalog
    It will create a new layer with a WFS or WCS connection, pointing to the specified GeoServer
    layer. In the case of a vector layer, it will also fetch its associated style and set it
    as the current style for the created QGIS layer
    '''
    layer = catalog.get_layer(typename)
    resource = layer.resource        
    
    if resource.resource_type == "featureType":
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typename': typename,
            'srsname': resource.projection
        }            
        url =  catalog.gs_base_url + "wfs?" + urllib.urlencode(params)  
        print url
        opengeo.config.iface.addVectorLayer(url, layer.name, "WFS") 
        try:
            sld = layer.default_style.sld_body
            print sld
        except Exception, e:        
            raise e        
    elif resource.resource_type == "coverage":
        pass


    


     
