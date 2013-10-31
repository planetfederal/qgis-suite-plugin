# -*- coding: utf-8 -*-

import sys
import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

from opengeo.qgis.catalog import *

def classFactory(iface):
    from opengeo.plugin import OpenGeoPlugin
    return OpenGeoPlugin(iface)
