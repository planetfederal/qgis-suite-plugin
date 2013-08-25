# -*- coding: utf-8 -*-

from opengeo.qgis.catalog import *

def classFactory(iface):
    from opengeo.plugin import OpenGeoPlugin
    return OpenGeoPlugin(iface)
