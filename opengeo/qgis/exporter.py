# -*- coding: utf-8 -*-


'''
This module provides method to export layers so they can be used as valid data 
for uploading to GeoServer.
'''

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo.qgis import utils
    

def exportVectorLayer(layer):

    settings = QSettings()
    systemEncoding = settings.value( "/UI/encoding", "System" )


    filename = str(layer.name())
    output = utils.getTempFilenameInTempFolder(filename + ".shp")
    provider = layer.dataProvider()
    
    if (not unicode(layer.source()).lower().endswith("shp") ):
        writer = QgsVectorFileWriter( output, systemEncoding, layer.pendingFields(), provider.geometryType(), layer.crs() )
        for feat in layer.getFeatures():
            writer.addFeature(feat)
        del writer
        return output
    else:
        return unicode(layer.source())



def exportRasterLayer(layer): 
    if (not unicode(layer.source()).lower().endswith("tif") ):        
        filename = str(layer.name())
        output = utils.getTempFilenameInTempFolder(filename + ".tif")
        writer = QgsRasterFileWriter(output)    
        writer.setOutputFormat("GTiff");
        writer.writeRaster(layer.pipe(), layer.width(), layer.height(), layer.extent(), layer.crs())
        del writer
        return output
    else:
        return unicode(layer.source())






