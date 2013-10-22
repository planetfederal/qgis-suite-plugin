# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/ext_libs'))

from opengeo.qgis.catalog import *

def classFactory(iface):
    from opengeo.plugin import OpenGeoPlugin
    return OpenGeoPlugin(iface)
