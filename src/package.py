#!/usr/bin/env python

# -*- coding: utf-8 -*-

import ConfigParser
from datetime import date
import os
import re
import xmlrpclib
import zipfile


SOURCES_DIR = "D:/github/suite-qgis-plugin/src/opengeo"
PACKAGE_DIR = "D:/"

SERVER = "plugins.qgis.org"
PORT = 80
PROTOCOL = "http"
END_POINT = "/plugins/RPC2/"

UPLOADER_NAME = "user"
UPLOADER_PASSWORD = "secret"

EXCLUDE_FILE = ["metadata.txt"]

def createPackage(pluginName):
    metadataFile = os.path.join(SOURCES_DIR, "metadata.txt")
    cfg = ConfigParser.SafeConfigParser()
    cfg.optionxform=str
    cfg.read(metadataFile)
    cfg.set("general", "version", "0.1-" + date.today().strftime("%Y%m%d"))

    # Add files to package
    with zipfile.ZipFile(os.path.join(PACKAGE_DIR, pluginName + ".zip"), "w", zipfile.ZIP_DEFLATED) as myZip:
        # Updated metadata.txt
        with open(os.path.join(PACKAGE_DIR, "metadata.txt"), "wb") as f:
            cfg.write(f)
        myZip.write(os.path.join(PACKAGE_DIR, "metadata.txt"), "opengeo/metadata.txt")

        # All other plugin files
        for root, dirs, files in os.walk(SOURCES_DIR):
            for f in files:
                if f not in EXCLUDE_FILE:
                    myZip.write(os.path.join(root, f), os.path.join(re.sub("^.*opengeo", "opengeo", root), f))                    
            if "test" in dirs:
                dirs.remove("test")


def upload(packagePath):
    # create URL for XML-RPC calls
    uri = "%s://%s:%s@%s:%s%s" % (PROTOCOL, UPLOADER_NAME, UPLOADER_PASSWORD, SERVER, PORT, END_POINT)

    server = xmlrpclib.ServerProxy(uri, verbose=False)
    try:
        pluginId, versionId = server.plugin.upload(xmlrpclib.Binary(open(packagePath).read()))
        print "Plugin ID: %s" % pluginId
        print "Version ID: %s" % versionId
    except xmlrpclib.Fault, err:
        print "A fault occurred"
        print "Fault code: %d" % err.faultCode
        print "Fault string: %s" % err.faultString


if __name__ == '__main__':
    pluginName = os.path.basename(SOURCES_DIR)
    createPackage(pluginName)
    pkg = os.path.join(PACKAGE_DIR, pluginName + ".zip")
    upload(pkg)
    # Cleanup
    os.remove(pkg)
    os.remove(os.path.join(PACKAGE_DIR, "metadata.txt"))
