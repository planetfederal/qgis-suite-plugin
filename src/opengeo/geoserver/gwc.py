from opengeo import httplib2
from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET
from urlparse import urlparse
from opengeo.geoserver.catalog import FailedRequestError

class Gwc(object):
        
    def __init__(self, catalog):
        self.catalog = catalog
        self.url = catalog.gs_base_url + 'gwc/rest/'
        http = httplib2.Http()
        http.add_credentials(catalog.username, catalog.password)
        netloc = urlparse(self.url).netloc
        http.authorizations.append(
            httplib2.BasicAuthentication(
                (catalog.username, catalog.password),
                netloc,
                self.url,
                {},
                None,
                None,
                http
            )
        )
        self.http = http 
       
    def layers(self):
        '''get a dict of layer->href'''
            
        url = self.url + 'layers.xml'
        headers, response = self.http.request(url, 'GET')
        if headers.status != 200: raise Exception('listing failed - %s, %s' %
                                                  (headers,response))
    
        # try to resolve layer if already configured
        dom = XML(response)
        layers = []
        for layer in dom.getchildren():
            els = layer.getchildren()            
            layers.append(self.layer(els[0].text))
        return layers 
    
    def layer(self, name):   
        layer = GwcLayer(self, name)                
        layer.fetch()
        return layer

    
        
    def addLayer(self, layer):        
        headers = {
            "Content-type": "text/xml"            
        }        
        message = layer.xml()        
        response = self.http.request(layer.href, "POST", message, headers)
        headers, body = response        
        if 400 <= int(headers['status']) < 600:            
            raise FailedRequestError(body)
        return response

    
class GwcLayer(object):

    def __init__(self, gwc, name, mimetypes = ['image/png'], 
                 gridsets = ['EPSG:4326', 'EPSG:900913'], metaWidth = 4, metaHeight = 4):
        self.gwc = gwc
        self.name = name
        self.gridsets = gridsets
        self.mimetypes = mimetypes
        self.metaWidth = metaWidth
        self.metaHeight = metaHeight
        
    def fetch(self):
        response, content = self.gwc.http.request(self.href)
        if response.status == 200:
            xml = XML(content)
            self.mimetypes = [mimetype.text for mimetype in xml.iter('string')]
            self.gridsets = [gridset.text for gridset in xml.iter('gridSetName')]
            self.metaWidth, self.metaHeight = [int(el.text) for el in xml.iter('int')]
        else:
            raise FailedRequestError(content)
    
    def xml(self):
        root = ET.Element('GeoServerLayer')
        enabled = ET.SubElement(root, 'enabled')
        enabled.text = 'true'
        name = ET.SubElement(root, 'name')
        name.text = self.name
        formats = ET.SubElement(root, 'mimeFormats')
        for mimetype in self.mimetypes:
            format = ET.SubElement(formats, 'string')
            format.text = mimetype            
        gridsubsets = ET.SubElement(root, 'gridSubsets')
        for gridset in self.gridsets:
            gridsubset = ET.SubElement(gridsubsets, 'gridSubset')
            gridsetName = ET.SubElement(gridsubset, 'gridSetName')
            gridsetName.text = gridset
        metaWH = ET.SubElement(root, 'metaWidthHeight')
        w = ET.SubElement(metaWH, 'int')
        w.text = str(self.metaWidth)    
        h = ET.SubElement(metaWH, 'int')
        h.text = str(self.metaHeight)
        return ET.tostring(root)

    @property
    def href(self):
        return self.gwc.url + "layers/" + self.name + ".xml"
    
    def update(self, mimetypes = ['image/png'], gridsets = ['EPSG:4326', 'EPSG900913'], metaWidth = 4, metaHeight = 4):        
        self.gridsets = gridsets
        self.mimetypes = mimetypes
        self.metaWidth = metaWidth
        self.metaHeight = metaHeight
        
        headers = {
            "Content-type": "text/xml"            
        }        
        message = self.xml()
        response = self.gwc.http.request(self.href, "POST", message, headers)
        headers, body = response        
        if 400 <= int(headers['status']) < 600:            
            raise FailedRequestError(body)
        return response
            
    def delete(self):
        headers = {
            "Content-type": "text/xml"        
        }
        
        response, content = self.gwc.http.request(self.href, "DELETE", headers=headers)

        if response.status == 200:
            return (response, content)
        else:
            raise FailedRequestError(str(response) + content)
            
    def truncate(self):
        headers = {
            "Content-type": "text/xml"        
        }
        url = self.gwc.url + "masstruncate"
        print url
        
        message = "<truncateLayer><layerName>"  + self.name + "</layerName></truncateLayer>"
        response, content = self.gwc.http.request(url, "POST", message, headers=headers)

        if response.status == 200:
            return (response, content)
        else:
            raise FailedRequestError(str(response) + content)

        
    def seed(self, operation, mimetype, gridset, minzoom, maxzoom, bbox):
        pass
    
    