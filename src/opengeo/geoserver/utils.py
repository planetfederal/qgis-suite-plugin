import urllib
from qgis.core import *
from opengeo.geoserver.layer import Layer

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
         
def mimeUri(element):
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
        return ':'.join([layertype, provider, layer.name, uri])