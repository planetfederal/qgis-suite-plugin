# -*- coding: utf-8 -*-

'''
Main functions for plugin functionality.
This is supposed to contain the functions to be called when using plugin 
functionality from the QGIS console
'''

import os
from qgis.core import *
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from opengeo.qgis import layers, exporter
from opengeo.geoserver.catalog import ConflictingDataError, UploadError
from opengeo.geoserver.catalog import Catalog as GSCatalog
from PyQt4 import QtXml
from opengeo.geoserver import utils
from opengeo.geoserver.sldadapter import adaptQgsToGs, adaptGsToQgs,\
    getGsCompatibleSld
    
def createGeoServerCatalog(service_url = "http://localhost:8080/geoserver/rest", 
                 username="admin", password="geoserver", disable_ssl_certificate_validation=False):
    catalog = GSCatalog(service_url, username, password, disable_ssl_certificate_validation)
    return OGCatalog(catalog)
    

class OGCatalog(object):
    '''
    This class is a wrapper for a catalog object, with convenience methods to use it with QGIS layers
    '''
    
    def __init__(self, catalog):
        self.catalog = catalog
    
    def publishStyle(self, layer, overwrite = False, name = None):
        '''
        Publishes the style of a given layer style in the specified catalog. If the overwrite parameter is True, 
        it will overwrite a style with that name in case it exists
        '''
        
        if isinstance(layer, basestring):
            layer = layers.resolveLayer(layer)         
        sld = getGsCompatibleSld(layer) 
        if sld is not None:       
            name = name if name is not None else layer.name()            
            self.catalog.create_style(name, sld, overwrite)
        return sld
       
    def getDataFromLayer(self, layer):
        '''
        Returns the data corresponding to a given layer, ready to be passed to the
        method in the Catalog class for uploading to the server.
        If needed, it performs and export to ensure that the file format is supported 
        by the upload API to be used for import. In that case, the data returned
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
    
    
    def createStore(self, layer, workspace=None, overwrite=True, name=None,
                           abstract=None, permissions=None, keywords=()):        
        '''Creates a datastore for the specified layer'''  
              
        if isinstance(layer, basestring):
            layer = layers.resolveLayer(layer)     
            
        name = name if name is not None else layer.name()
                    
        try:
            if layer.type() == layer.RasterLayer:
                data = self.getDataFromLayer(layer)
                self.catalog.create_coveragestore(name,
                                           data,
                                           workspace=workspace,
                                           overwrite=overwrite)      
            elif layer.type() == layer.VectorLayer:
                provider = layer.dataProvider()
                if provider.name() == 'postgres':                                        
                    connName = self.getConnectionNameFromLayer(layer)
                    uri = QgsDataSourceURI(provider.dataSourceUri())                                                                     
                    self.catalog.create_pg_featurestore(connName,                                           
                                           workspace = workspace,
                                           overwrite = overwrite,
                                           host = uri.host(),
                                           database = uri.database(),
                                           schema = uri.schema(),
                                           port = uri.port(),
                                           user = uri.username(),
                                           passwd = uri.password())  
                    self.catalog.create_pg_featuretype(uri.table(), connName, workspace, layer.crs().authid())
                else:                             
                    data = self.getDataFromLayer(layer)
                    self.catalog.create_shp_featurestore(name,
                                           data,
                                           workspace=workspace,
                                           overwrite=overwrite)
            else:
                msg = layer.name() + ' is not a valid raster or vector layer'
                raise Exception(msg)
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
        resource = self.catalog.get_resource(layer.name())
        if resource is not None:
            assert resource.name == layer.name()
        else:
            msg = ('could not create layer %s.' % layer.name())
            raise Exception(msg)
       
        if resource.latlon_bbox is None:
            box = resource.native_bbox[:4]
            minx, maxx, miny, maxy = [float(a) for a in box]
            if -180 <= minx <= 180 and -180 <= maxx <= 180 and \
                    -90 <= miny <= 90 and -90 <= maxy <= 90:
                resource.latlon_bbox = resource.native_bbox
                resource.projection = "EPSG:4326"
                self.catalog.save(resource)
            else:
                msg = ('Could not set projection for layer '
                       '[%s]. the layer has been created, but its projection should be set manually.')
                raise Exception(msg % layer.name())
            
    def getConnectionNameFromLayer(self, layer):
        connName = "postgis_store"
        uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())                
        host = uri.host()
        database = uri.database()
        port = uri.port()                
        settings = QSettings()
        settings.beginGroup(u'/PostgreSQL/connections')
        for name in settings.childGroups():
            settings.beginGroup(name)
            host2 = str(settings.value('host'))
            database2 = str(settings.value('database'))
            port2 = str(settings.value('port'))
            settings.endGroup()
            if port == port2 and database == database2 and host == host2:
                connName = name + "_" + str(uri.schema()) 
        settings.endGroup()
        return connName  
              
    def publishGroup(self, name, workspace=None, overwrite=False, overwriteLayers = False):
        
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
            raise Exception("The specified group does not exist")
        
        group = groups[name]
        
        for layer in group:
            layer = self.catalog.get_layer(layer)
            if layer is None:
                self.publishLayer(layer, self.catalog, workspace, None, overwrite)
                
        layergroup = self.catalog.create_layergroup(name, group, group)
        self.catalog.save(layergroup)
        
    def publishLayer (self, layer, workspace=None, overwrite=True, name=None,
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
        
        name = name if name is not None else layer.name()
          
        sld = self.publishStyle(layer, overwrite, name)
            
        self.createStore(layer, workspace, overwrite, name)      
    
        if sld is not None:
            #assign style to created store  
            publishing = self.catalog.get_layer(name)        
            publishing.default_style = self.catalog.get_style(name)
            self.catalog.save(publishing)
            
    def addLayerToProject(self, name):
        '''
        Adds a new layer to the current project based on a layer in a GeoServer catalog
        It will create a new layer with a WFS or WCS connection, pointing to the specified GeoServer
        layer. In the case of a vector layer, it will also fetch its associated style and set it
        as the current style for the created QGIS layer
        '''
        layer = self.catalog.get_layer(name)
        if layer is None:
            raise Exception ("A layer with the name '" + name + "' was not found in the catalog")
            
        resource = layer.resource        
        uri = utils.layerUri(layer)                        
        if resource.resource_type == "featureType":                    
            qgslayer = QgsVectorLayer(uri, layer.name, "WFS") 
            err = False
            try:
                sld = layer.default_style.sld_body  
                sld = adaptGsToQgs(sld)              
                node = QtXml.QDomDocument()  
                node.setContent(sld)              
                qgslayer.readSld(node, "")                
            except Exception, e:        
                err = True
            QgsMapLayerRegistry.instance().addMapLayers([qgslayer])
            if err:
               raise Exception ("Layer was added, but style could not be set (maybe GeoServer layer is missing default style)")        
        elif resource.resource_type == "coverage":                        
            qgslayer = QgsRasterLayer(uri, name, "wcs" )            
            QgsMapLayerRegistry.instance().addMapLayers([qgslayer])

                        