import urllib
from qgis.core import *
from opengeo.geoserver.layer import Layer
from opengeo.postgis.table import Table

def layerUri(layer):
    resource = layer.resource                
    if resource.resource_type == 'featureType':                 
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typename': layer.name,
            'srsname': resource.projection
        }                        
        uri = layer.catalog.gs_base_url + 'wfs?' + urllib.unquote(urllib.urlencode(params))
        return uri                                                            
    else:        
        uri = QgsDataSourceURI()                    
        uri.setParam ("url", layer.catalog.gs_base_url + "wcs")
        identifier = layer.resource.workspace.name + ":" + layer.resource.name            
        uri.setParam ( "identifier", identifier)
        return str(uri.encodedUri())
         
def layerMimeUri(element):
    if isinstance(element, Layer):
        layer = element
        uri = layerUri(layer)
        resource = layer.resource                
        if resource.resource_type == 'featureType': 
            layertype = 'vector'
            provider = 'WFS'                                                                                          
        else:
            layertype = 'raster'
            provider = 'wcs'       
        escapedName = layer.name.replace( ":", "\\:" );
        escapedUri = uri.replace( ":", "\\:" );         
        mimeUri = ':'.join([layertype, provider, escapedName, escapedUri])        
        return mimeUri
    
def tableUri(table):
        geodb = table.conn.geodb
        uri = QgsDataSourceURI()    
        uri.setConnection(geodb.host, str(geodb.port), geodb.dbname, geodb.user, geodb.passwd)    
        uri.setDataSource(table.schema, table.name, table.geomfield) 
        return uri.uri()
             
def tableMimeUri(table):
    if isinstance(table, Table):        
        uri = tableUri(table)                             
        return ':'.join(["vector", "postgres", table.name, uri])    