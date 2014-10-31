import os
import tempfile
from qgis.core import *

TEMP_CERT_FILE_PREFIX = "tmppki_"

def getPemPkiPaths(authid):
    configpki = QgsAuthConfigPkiPaths()
    QgsAuthManager.instance().loadAuthenticationConfig(authid, configpki, True)
    certfile = _getAsPem(configpki.certId, configpki.certAsPem)
    keyfile = _getAsPem(configpki.keyId, configpki.keyAsPem)
    cafile = _getAsPem(configpki.issuerId, configpki.issuerAsPem)

    return certfile, keyfile, cafile

def _getAsPem(self, pathMethod, stringMethod):
    filename = pathMethod()
    if os.path.splitext(filename)[0].lower() != "pem":
        s = stringMethod()
        fd, filename = tempfile.mkstemp(".pem")
        f = os.fdopen(fd,'w')
        f.write(s)
        os.close(fd)
    return filename

def removePkiTempFiles(catalogs):
    for catalog in catalogs:
        removeCatalogPkiTempFiles(catalog)

def removeCatalogPkiTempFiles(catalog):
    if catalog.certfile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.certfile)
    if catalog.keyfile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.keyfile)
    if catalog.cafile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.cafile)

