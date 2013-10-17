from opengeo import httplib2
from xml.etree.ElementTree import XML
from urlparse import urlparse

class Wps(object):
    
    def __init__(self, catalog):
        self.catalog = catalog
        self.url = catalog.gs_base_url + 'wps'
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
        
    def processes(self):     
        url = self.url + '?Request=GetCapabilities&Service=WPS&AcceptVersions=1.0.0'                                
        headers, response = self.http.request(url, 'GET')
        if headers.status != 200: raise Exception('Processes listing failed - %s, %s' %
                                                 (headers,response))
        response = response.replace('ows:','')
        dom = XML(response)                
        processes = [p.text for p in dom.iter() if 'Title' in p.tag]        
        return processes