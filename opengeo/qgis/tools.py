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

def defaultCatalog():
    return Catalog("http://localhost:8080/geoserver/rest")

def publishStyle(layerName, catalog=defaultCatalog(), name=None, params=[], overwrite = False):
 
    layer = layers.resolveLayer(layerName)    
    name = layer.name() if name is None else name
    sld = getStyleAsSLD(layer)
    print sld    
    catalog.create_style(name, sld, overwrite)
    
    

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
    if layer.type() == layer.RasterLayer:
        pass      
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


def createStore(layerName, catalog=defaultCatalog(), workspace=None, name=None, overwrite=False, title=None,
                       abstract=None, permissions=None, keywords=()):
    
    '''Creates a datastore for the specified layer'''
    
    layer = layers.resolveLayer(layerName)    
    name = layer.name() if name is None else name

    if layer.type() == layer.RasterLayer:
        create_store_and_resource= catalog.create_coveragestore      
    elif layer.type() == layer.VectorLayer:
        create_store_and_resource= catalog.create_featurestore
    else:
        msg = name + ' is not a valid raster or vector layer'
        raise Exception(msg)

    #convert to a format that can be used for publication, if needed    
    data = getDataFromLayer(layer)
    
    #TODO: validation of the name
    #TODO: in case the name already exist, prompt user to ask for overwrite
    #TODO: manage PostGIS datastore type


    try:
        create_store_and_resource(name,
                                   data,
                                   workspace=workspace,
                                   overwrite=overwrite)
    except UploadError, e:
        msg = ('Could not save the layer %s, there was an upload '
               'error: %s' % (name, str(e)))
        e.args = (msg,)
        raise
    except ConflictingDataError, e:
        # A datastore of this name already exists
        msg = ('GeoServer reported a conflict creating a store with name %s: '
               '"%s". This should never happen because a brand new name '
               'should have been generated. But since it happened, '
               'try renaming the file or deleting the store in '
               'GeoServer.' % (name, str(e)))
        e.args = (msg,)
        raise


    # Verify the resource was created
    gs_resource = catalog.get_resource(name)
    if gs_resource is not None:
        assert gs_resource.name == name
    else:
        msg = ('The QGS Bridge encounterd problems when creating layer %s.'
               'It cannot find the Layer that matches this Workspace.'
               'try renaming your files.' % name)
        raise Exception(msg)

    #Make sure our data always has a valid projection
    # FIXME: Put this in gsconfig.py
    
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
            raise Exception(msg % name)
    

def publishLayer (layerName, catalog=defaultCatalog(), workspace=None, name=None, overwrite=False, title=None,
                       abstract=None, permissions=None, keywords=()):
    '''
    Publishes a QGIS layer. 
    It creates the corresponding store and the layer itself 
    If the layer is a group layer, it publishes all the layers individually and then creates 
    the layer group in the server
    
    layerName: the layer to publish, specified by its name in the QGIS TOC.
        
    catalog. A catalog object with information about the URL of the service to publish to.
    
    workspace: the workspace to publish to. USes the default project if not passed 
    or None 
    
    name: the name for the published layer. Uses the QGIS layer name if not passed 
    or None
       
    params: a dict with additional configuration parameters if needed
    
    '''
    
    layer = layers.resolveLayer(layerName)    
    name = layer.name() if name is None else name
 
    #publish style
    publishStyle(layerName, catalog, name)
    
    #create store
    createStore(layerName, catalog, name)      
    
    from threading import settrace

    import sys
    sys.path.append("D:\eclipse_old\plugins\org.python.pydev_2.6.0.2012062818\pysrc")
    from pydevd import *
    settrace()
    
    #assign style to created store  
    publishing = catalog.get_layer(name)        
    #FIXME: Should we use the fully qualified typename?
    publishing.default_style = catalog.get_style(name)
    catalog.save(publishing)
