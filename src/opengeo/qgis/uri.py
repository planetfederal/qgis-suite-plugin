import urllib
from qgis.core import *
from geoserver.layer import Layer
from opengeo.postgis.table import Table
from opengeo.geoserver.pki import PKICatalog

def layerUri(layer):
    resource = layer.resource
    catalog = layer.catalog
    if resource.resource_type == 'featureType':
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typename': resource.workspace.name + ":" + layer.name,
            'srsname': resource.projection,
            'password': catalog.password,
            'username': catalog.username
        }
        service = 'wfs'
    else:
        params = {
            'identifier': layer.resource.workspace.name + ":" + layer.resource.name
        }
        service = 'wcs'
    if isinstance(catalog, PKICatalog):
        params['certid'] = catalog.cert
        params['keyid'] = catalog.key
        if catalog.ca_cert is not None:
            params['issuerid'] = catalog.ca_cert
    uri = layer.catalog.gs_base_url + service +'?' + urllib.unquote(urllib.urlencode(params))
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