import os
import tempfile
from qgis.core import *
import uuid

TEMP_CERT_FILE_PREFIX = "tmppki_"

_certFolder = None

def certFolder():
    global _certFolder
    if _certFolder is None:
        _certFolder = tempfile.mkdtemp()
    return _certFolder

def getPemPkiPaths(authid):
    configpki = QgsAuthConfigPkiPaths()
    QgsAuthManager.instance().loadAuthenticationConfig(authid, configpki, True)
    certfile = _getAsPem(configpki.certId, configpki.certAsPem)
    if configpki.keyPassphrase():
        keyfile = _getAsPem(lambda: "file.notpem", lambda: configpki.keyAsPem(True))
    else:
        keyfile = _getAsPem(configpki.keyId, lambda: configpki.keyAsPem(True)[0])
    cafile = _getAsPem(configpki.issuerId, configpki.issuerAsPem)

    return certfile, keyfile, cafile

def _getAsPem(pathMethod, stringMethod):
    filename = pathMethod()
    if os.path.splitext(filename)[0].lower() != ".pem":
        s = stringMethod()
        filename = os.path.join(certFolder(), str(uuid.uuid4()) + ".pem")
        with open(filename,'w') as f:
            f.write(s)
    return filename

def removePkiTempFiles(catalogs):
    for catalog in catalogs.values():
        removeCatalogPkiTempFiles(catalog)

def removeCatalogPkiTempFiles(catalog):
    if catalog is None:
        return
    if catalog.certfile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.certfile)
    if catalog.keyfile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.keyfile)
    if catalog.cafile.startswith(TEMP_CERT_FILE_PREFIX):
        os.remove(catalog.cafile)

