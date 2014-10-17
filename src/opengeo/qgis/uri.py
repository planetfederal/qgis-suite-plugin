import urllib
from qgis.core import *
from geoserver.layer import Layer
from opengeo.postgis.table import Table
from opengeo.geoserver.pki import PKICatalog

def layerUri(layer):
    resource = layer.resource
    catalog = layer.catalog
    def addAuth(_params):
        authid = catalog.authid
        if authid is not None:
            _params['authid'] = catalog.authid
        else:
            _params['password'] = catalog.password
            _params['username'] = catalog.username
    if resource.resource_type == 'featureType':
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typename': resource.workspace.name + ":" + layer.name,
            'srsname': resource.projection,
        }
        addAuth(params)
        uri = layer.catalog.gs_base_url + 'wfs?' + urllib.unquote(urllib.urlencode(params))
    else:
        params = {
            'identifier': layer.resource.workspace.name + ":" + layer.resource.name,
            'format': 'GeoTIFF',
            'url': layer.catalog.gs_base_url + 'wcs',
            'cache': 'PreferNetwork'
        }
        addAuth(params)
        uri = urllib.unquote(urllib.urlencode(params))


    return uri

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
        escapedName = resource.title.replace( ":", "\\:" );
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