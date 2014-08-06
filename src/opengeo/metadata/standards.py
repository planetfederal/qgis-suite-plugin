import os
from qgis.core import *
import codecs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4.QtXmlPatterns import QXmlQuery, QXmlSchema, QXmlSchemaValidator
from error_handler import ErrorHandler

class Standard(object):

    def _setNodeValue(self, dom, nodeName, value):
        node = dom.elementsByTagName(nodeName).at(0)
        print node
        if node is None:
            node = dom.elementsByTagName(nodeName.split(":")[1]).at(0)
            print node
            if node is None:
                print "return"
                return
        if not node.hasChildNodes():
            textNode = node.ownerDocument().createTextNode(value)
            node.appendChild(textNode)
        else:
            node.childNodes().at(0).setNodeValue(value)

    def setExtent(self, dom, bbox):
        self._setNodeValue(dom, self.xminNode, str(bbox[0]))
        self._setNodeValue(dom, self.xmaxNode, str(bbox[1]))
        self._setNodeValue(dom, self.yminNode, str(bbox[2]))
        self._setNodeValue(dom, self.ymaxNode, str(bbox[3]))

    def getHtml(self, md):
        xsltFile = QFile(self.xsltFilePath)
        xsltFile.open(QIODevice.ReadOnly)
        xslt = unicode(xsltFile.readAll())
        xsltFile.close()

        qry = QXmlQuery(QXmlQuery.XSLT20)

        self.handler = ErrorHandler()
        qry.setMessageHandler(self.handler)

        qry.setFocus(md)
        qry.setQuery(xslt)

        return qry.evaluateToString()

    def validate(self, md):
        schema = QXmlSchema()
        schemaUrl = QUrl(self.xsdFilePath)

        schema.load(schemaUrl)
        if not schema.isValid():
            raise Exception("Could not load schema for validation")

        validator = QXmlSchemaValidator(schema)
        handler = ErrorHandler()
        validator.setMessageHandler(handler)

        if not validator.validate(md):
            raise Exception("Metadata did not validate")

    def getTemplate(self, layer):
        filename = self.name + "_vector.xml" if layer.type() == QgsMapLayer.VectorLayer else self.name + "_raster.xml"
        templatePath = os.path.join(os.path.dirname(__file__), "templates", filename)
        f = codecs.open(templatePath, "r", encoding="utf-8")
        content = f.read()
        f.close()
        return content

class IsoStandard(Standard):

    name = "iso"
    xsdFilePath = os.path.join(os.path.dirname(__file__), "xsd", "iso", "gmd", "gmd.xsd")
    xsltFilePath =  os.path.join(os.path.dirname(__file__), "xsl", "iso19115.xsl")
    ymaxNode = "gmd:northBoundLatitude"
    yminNode = "gmd:southBoundLatitude"
    xmaxNode = "gmd:eastBoundLongitude"
    xminNode = "gmd:westBoundLongitude"

    def _setNodeValue(self, dom, nodeName, value):
        node = dom.elementsByTagName(nodeName).at(0)
        if node.isNull():
            node = dom.elementsByTagName(nodeName.split(":")[1]).at(0)
            if node.isNull():
                return
        node = node.firstChild()
        if not node.hasChildNodes():
            textNode = node.ownerDocument().createTextNode(value)
            node.appendChild(textNode)
        else:
            node.childNodes().at(0).setNodeValue(value)

    def verify(self, md):
        return md.find("MD_Metadata") >= 0 or md.find("MI_Metadata") >= 0

class FgdcStandard(Standard):

    name = "fgdc"
    xsdFilePath = os.path.join(os.path.dirname(__file__), "xsd", "fgdc", "fgdc-std-001-1998.xsd")
    xsltFilePath =  os.path.join(os.path.dirname(__file__), "xsl", "fgdc.xsl")

    def verify(self, md):
        return md.find("idinfo") >= 0 and md.find("metainfo") >= 0

class UnknownStandard(Standard):
    pass


def tryDetermineStandard(metadata):
    std = [FgdcStandard(), IsoStandard()]
    for s in std:
        if s.verify(metadata):
            return s

    return UnknownStandard()




