from geoserver.catalog import Catalog
import httplib2
from PyQt4.QtCore import *
from gsimporter.client import Client, _Client

class PKICatalog(Catalog):

    def __init__(self, service_url, key, cert):
        self.key = key
        self.cert = cert
        self.service_url = service_url
        if self.service_url.endswith("/"):
            self.service_url = self.service_url.strip("/")
        ca_cert = QSettings().value("/OpenGeo/Settings/GeoServer/CACertsFile", "")
        self.ca_cert = ca_cert if (str(ca_cert) != unicode('NULL') and unicode(ca_cert).strip()) != "" else None
        self.http = httplib2.Http(ca_certs = self.ca_cert, disable_ssl_certificate_validation = False)
        self.http.add_certificate(key, cert, '')
        self._cache = dict()
        self._version = None

class PKIClient(Client):

    def __init__(self, url, key, cert):
        self.client = _PKIClient(url, key, cert)

    def __getstate__(self):
        cl = self.client
        return {'url':cl.service_url,'keyfile':cl.key,'certfile':cl.cert}
    def __setstate__(self,state):
        self.client = _PKIClient(state['url'],state['keyfile'],state['certfile'])

class _PKIClient(_Client):

    def __init__(self, url, key, cert):
        self.service_url = url
        if self.service_url.endswith("/"):
            self.service_url = self.service_url.strip("/")
        ca_cert = QSettings().value("/OpenGeo/Settings/GeoServer/CACertsFile", "")
        self.ca_cert = ca_cert if (str(ca_cert) != unicode('NULL') and unicode(ca_cert).strip()) != "" else None
        self.http = httplib2.Http(ca_certs = self.ca_cert, disable_ssl_certificate_validation = False)
        self.http.add_certificate(key, cert, '')

