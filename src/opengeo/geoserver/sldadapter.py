'''
methods tto convert the SLD produced by GeoServer (1.0) to the SLD produced by QGIS (1.1), and also the other way round.
This is a quick and dirty solution until both programs support the same specification
'''

import re
import os
from PyQt4.QtXml import *

def adaptQgsToGs(sld, layer):
    print sld
    sld = sld.replace("se:SvgParameter","CssParameter")
    sld = sld.replace("1.1.","1.0.")
    sld = sld.replace("\t","")
    sld = sld.replace("\n","")
    sld = re.sub("\s\s+" , " ", sld)
    sld = re.sub("<ogc:Filter>[ ]*?<ogc:Filter>","<ogc:Filter>", sld)
    sld = re.sub("</ogc:Filter>[ ]*?</ogc:Filter>","</ogc:Filter>", sld)   
    if layer.hasScaleBasedVisibility():
        s = ("<MinScaleDenominator>" + str(layer.minimumScale()) + 
        "</MinScaleDenominator><MaxScaleDenominator>" + str(layer.maximumScale()) + "</MaxScaleDenominator>")
        sld = sld.replace("<se:Rule>", "<se:Rule>" + s)
    print sld        
    
    return sld

def adaptGsToQgs(sld):
    return sld

def getGsCompatibleSld(layer):
    sld = getStyleAsSld(layer)
    if sld is not None:
        return adaptQgsToGs(sld, layer)
    else:
        return None

def getStyleAsSld(layer):        
    if layer.type() == layer.VectorLayer:  
        document = QDomDocument()
        header = document.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"UTF-8\"" )
        document.appendChild( header )
            
        root = document.createElementNS( "http://www.opengis.net/sld", "StyledLayerDescriptor" )
        root.setAttribute( "version", "1.1.0" )
        root.setAttribute( "xsi:schemaLocation", "http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd" )
        root.setAttribute( "xmlns:ogc", "http://www.opengis.net/ogc" )
        root.setAttribute( "xmlns:se", "http://www.opengis.net/se" )
        root.setAttribute( "xmlns:xlink", "http://www.w3.org/1999/xlink" )
        root.setAttribute( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance" )
        document.appendChild( root )
    
        namedLayerNode = document.createElement( "NamedLayer" )
        root.appendChild( namedLayerNode )
                
        errorMsg = ""
                
        layer.writeSld(namedLayerNode, document, errorMsg)                        
        
        return unicode(document.toString(4))
    elif layer.type() == layer.RasterLayer: 
        #QGIS does not support SLD for raster layers, so we have this workaround
        sldpath = os.path.join(os.path.dirname(__file__), "..", "resources")
        if layer.bandCount() == 1:
            sldfile = os.path.join(sldpath, "grayscale.sld")
        else:
            sldfile = os.path.join(sldpath, "rgb.sld")                
        with open(sldfile, 'r') as f:
            sld = f.read()
        return sld
    else:
        return None