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
from opengeo.qgis import layers, exporter, utils
from opengeo.geoserver.catalog import ConflictingDataError, UploadError
from opengeo.geoserver.catalog import Catalog as GSCatalog
import urllib
import re
from opengeo import httplib2
from PyQt4 import QtXml
    
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
    
    def publish_style(self, layer, overwrite = False):
     
        '''
        Publishes the style of a given layer style in the specified catalog. If the overwrite parameter is True, 
        it will overwrite a style with that name in case it exists
        '''
        
        if isinstance(layer, basestring):
            layer = layers.resolve_layer(layer)         
        sld = self.get_style_as_sld(layer)
        print sld  
        self.catalog.create_style(layer.name(), sld, overwrite)
        
        
    
    def publishProject(self):
        pass
       
    def get_style_as_sld(self, layer):
        
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
    
    
    def get_data_from_layer(self, layer):
        '''
        Returns the data corresponding to a given layer, ready to be passed to the
        method in the Catalog class for uploading to the server.
        If needed, it performs and export to ensure that the file format is supported 
        by the upload API to be used for import. In that case, the data returned
        will point to the exported copy of the data, not the original data source
        '''
        if layer.type() == layer.RasterLayer:
            data = exporter.export_raster_layer(layer)                              
        else:      
            filename = exporter.export_vector_layer(layer)        
            basename, extension = os.path.splitext(filename)        
            data = {
                'shp': basename + '.shp',
                'shx': basename + '.shx',
                'dbf': basename + '.dbf',
                'prj': basename + '.prj'
            }
        return data
    
    
    def get_db_connection_params(self, layer):
        tags = re.findall("*.?=*.? ", unicode(layer.source()))
        params = {}
        for tag in tags:            
            k, v = tag.replace('"', "").replace("'","").split("=")
            params[k] = v
        keys = [u'port', u'dbname', u'schema', u'host']
        params = {key: value for (key, value) in params if k in keys}
    
    def create_store(self, layer, workspace=None, overwrite=False, title=None,
                           abstract=None, permissions=None, keywords=()):
        
        '''Creates a datastore for the specified layer'''
        
        if isinstance(layer, basestring):
            layer = layers.resolve_layer(layer)     
            
        try:
            if layer.type() == layer.RasterLayer:
                data = self.get_data_from_layer(layer)
                self.catalog.create_coveragestore(layer.name(),
                                           data,
                                           workspace=workspace,
                                           overwrite=overwrite)      
            elif layer.type() == layer.VectorLayer:
                provider = layer.dataProvider()
                if provider.name() == 'postgres':                    
                    uri = QgsDataSourceURI(provider.dataSourceUri())
                    #TODO: check that a PostGIS store with those params does not exist                    
                    self.catalog.create_pg_featurestore("postgis_store",                                           
                                           workspace = workspace,
                                           overwrite = overwrite,
                                           host = uri.host(),
                                           database = uri.database(),
                                           schema = uri.schema(),
                                           port = uri.port(),
                                           user = uri.username(),
                                           passwd = uri.password())  
                    self.catalog.create_pg_featuretype(uri.table(),"postgis_store")
                else:                             
                    data = self.get_data_from_layer(layer)
                    self.catalog.create_shp_featurestore(layer.name(),
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
                msg = ('GeoServer failed to detect the projection for layer '
                       '[%s]. It doesn\'t look like EPSG:4326, so backing out '
                       'the layer.')
                raise Exception(msg % layer.name())
            
    def publish_group(self, name, workspace=None, overwrite=False, overwriteLayers = False):
        
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
        
        groups = layers.get_groups()
        if name not in groups:
            raise Exception("the specified group does not exist")
        
        group = groups[name]
        
        for layer in group:
            layer = self.catalog.get_layer(layer)
            if layer is None:
                self.publish_layer(layer, self.catalog, workspace, None, overwrite)
                
        layergroup = self.catalog.create_layergroup(name, group, group)
        self.catalog.save(layergroup)
        
    def publish_layer (self, layer, workspace=None, overwrite=True, title=None,
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
            layer = layers.resolve_layer(layer)          
          
        if layer.type() == layer.VectorLayer:  
            #publish style
            self.publish_style(layer,overwrite)
        
        #create store
        self.create_store(layer, workspace, overwrite)      
    
        if layer.type() == layer.VectorLayer:
            #assign style to created store  
            publishing = self.catalog.get_layer(layer.name())        
            #FIXME: Should we use the fully qualified typename?
            publishing.default_style = self.catalog.get_style(layer.name())
            self.catalog.save(publishing)
            
    def add_layer_to_project(self, name):
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
        
        if resource.resource_type == "featureType":
            params = {
                'service': 'WFS',
                'version': '1.0.0',
                'request': 'GetFeature',
                'typename': name,
                'srsname': resource.projection
            }            
            url =  self.catalog.gs_base_url + "wfs?" + urllib.urlencode(params)              
            qgslayer = QgsVectorLayer(url, layer.name, "WFS") 
            try:
                sld = layer.default_style.sld_body
                stylefile = utils.temp_filename("sld")
                with open(stylefile, 'w') as f:
                    f.write(sld)     
                print sld                       
                node = QtXml.QDomDocument()
                node.setContent(sld)
                qgslayer.readSld(node, "")
                QgsMapLayerRegistry.instance().addMapLayers([qgslayer])
            except Exception, e:        
                raise e        
        elif resource.resource_type == "coverage":
                from lxml import etree
                client = httplib2.Http()
                description_url = self.catalog.gs_base_url + "wcs?" + urllib.urlencode({
                        "service": "WCS",
                        "version": "1.0.0",
                        "request": "DescribeCoverage",
                        "coverage": self.typename
                    })
                content = client.request(description_url)[1]
                doc = etree.fromstring(content)
                extent = doc.find(".//%(gml)slimits/%(gml)sGridEnvelope" % {"gml": "{http://www.opengis.net/gml}"})
                low = extent.find("{http://www.opengis.net/gml}low").text.split()
                high = extent.find("{http://www.opengis.net/gml}high").text.split()
                w, h = [int(h) - int(l) for (h, l) in zip(high, low)]

                bbox = self.resource.latlon_bbox
                crs = 'EPSG:4326'  if bbox[4] is None else bbox[4]
                bbox_string = ",".join([bbox[0], bbox[2], bbox[1], bbox[3]])
                
        
                url = self.catalog.gs_base_url + "wcs?" + urllib.urlencode({
                        "service": "WCS",
                        "version": "1.0.0",
                        "request": "GetCoverage",
                        "CRS": crs,
                        "height": h,
                        "width": w,
                        "coverage": self.typename,
                        "bbox": bbox_string,
                        "format": "geotiff"
                    })


    

    


     
