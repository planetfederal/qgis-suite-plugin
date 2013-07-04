# -*- coding: utf-8 -*-



#===============================================================================
# from sextante.tools.general import runalg, runandload, alghelp, alglist, algoptions, load, extent, getobject
# from sextante.tools.vector import getfeatures, spatialindex, values, uniquevalues
# from sextante.tools.raster import scanraster
# from sextante.tests.TestData import loadTestData
#===============================================================================

from opengeo.qgis.tools import publishLayer, publishStyle, createStore

def classFactory(iface):
    from opengeo.plugin import OpenGeoPlugin
    return OpenGeoPlugin(iface)
