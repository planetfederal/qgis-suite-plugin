import os
import uuid
import time
from PyQt4.QtCore import *
import urllib
from qgis.core import *
from opengeo.core.layer import Layer

def tempFolder():
    tempDir = os.path.join(unicode(QDir.tempPath()), "suiteplugin")
    if not QDir(tempDir).exists():
        QDir().mkpath(tempDir)
    return unicode(os.path.abspath(tempDir))

def tempFilename(ext):
    path = tempFolder()
    ext = "" if ext is None else ext
    filename = path + os.sep + str(time.time())  + "." + ext
    return filename

def tempFilenameInTempFolder(basename):
    '''returns a temporary filename for a given file, putting it into a temp folder but not changing its basename'''
    path = tempFolder()
    folder = os.path.join(path, str(uuid.uuid4()).replace("-",""))
    mkdir(folder)
    filename =  os.path.join(folder, basename)
    return filename

def mkdir(newdir):
    if os.path.isdir(newdir):
        pass
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        if tail:
            os.mkdir(newdir)

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
