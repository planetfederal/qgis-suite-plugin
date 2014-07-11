from geoserver.catalog import Catalog
import httplib2
from PyQt4.QtCore import *

class PKICatalog(Catalog):

    def __init__(self, service_url, key, cert):
        self.key = key
        self.cert = cert
        self.service_url = service_url
        if self.service_url.endswith("/"):
            self.service_url = self.service_url.strip("/")
        ca_cert = QSettings().value("/OpenGeo/Settings/General/CACertsFile", "")
        self.ca_cert = ca_cert if (ca_cert != NULL and ca_cert.strip()) != "" else None
        self.http = httplib2.Http(ca_cert = self.ca_cert, disable_ssl_certificate_validation = False)
        self.http.add_certificate(key, cert)     
        self._cache = dict()
        self._version = None

                