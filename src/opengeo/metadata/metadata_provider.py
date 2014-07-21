# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
#
# Copyright (C) 2011 BV (enickulin@bv.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************
from qgis.core import *
from os import path, remove
import codecs
from error_handler import ErrorHandler
from standard import MetaInfoStandard
from PyQt4.QtCore import *
from PyQt4.QtGui import *

NO_PSYCOPG2 = False
try:
  import psycopg2
except:
  NO_PSYCOPG2 = True


class MetadataProvider:
  tempFilePaths = []

  def __del__(self):
    for tempFilePath in self.tempFilePaths:
      if path.exists(tempFilePath):
        try:
          remove(tempFilePath)
        except:
          pass

  def checkExists(self):
    raise Exception()

  # always return unicode string!
  def getMetadata(self):
    raise Exception()

  # metadata - unicode string!
  def setMetadata(self, metadata):
    raise Exception()


  def exportToFile(self, outputFilePath):
    metaFile = codecs.open(outputFilePath, "w", encoding="utf-8")
    metaFile.write(self.getMetadata())
    metaFile.close()

  def importFromFile(self, inputFilePath):
    #read metadata from file
    metaFile = codecs.open(inputFilePath, "r", encoding="utf-8")
    content = metaFile.read()
    metaFile.close()
    
    # check matadata standard
    standard = MetaInfoStandard.tryDetermineStandard(content)
    if standard == MetaInfoStandard.UNKNOWN:
        raise Exception("Unsupported metadata standard. Only ISO19115 and FGDC are supported")
    if standard == MetaInfoStandard.FGDC:
        from PyQt4.QtXmlPatterns import QXmlSchema, QXmlSchemaValidator
        # setup xml schema
        schema = QXmlSchema()
    
        # setup handler
        self.handler = ErrorHandler("Metadata is invalid")
        schema.setMessageHandler(self.handler)
    
        # load schema from file
        xsdFilePath = self.pluginPath + '/xsd/fgdc/fgdc-std-001-1998.xsd'
        #if standard != MetaInfoStandard.FGDC:
        #    xsdFilePath = 'c:/xsd/gml/basicTypes.xsd' #   gmd/gmd.xsd'
        schemaUrl = QUrl(xsdFilePath)
        loadResult = schema.load(schemaUrl)
        if not loadResult or self.handler.errorOccured:
            raise Exception("Could not load schema for validation")
    
        #setup validator
        validator = QXmlSchemaValidator(schema)
        validator.setMessageHandler(self.handler)
    
        #validate
        metadata = self.metaProvider.getMetadata().encode('utf-8')
        if not validator.validate(metadata):
            raise Exception("Metadata did not validate")
    
    #save to provider
    self.setMetadata(content)

  @staticmethod
  def isLayerSupported(layer):
    # Null layers are not supported :)
    if layer is None:
      return (False, "Null layers are not supported :)")

    # Only vector and raster layers are supported now
    if layer.type() != QgsMapLayer.VectorLayer and layer.type() != QgsMapLayer.RasterLayer:
      return (False, "Only vector and raster layers are supported")

    # Check raster layers
    if layer.type() == QgsMapLayer.RasterLayer:
      # Only gdal-based raster are supported now!
      if layer.providerType() != "gdal":
        return (False, "Only gdal-based raster are supported")
      # Only file based rasters are supported now
      if not path.exists(unicode(layer.source())):
        return (False, "Only file based rasters are supported")

    #Check vector layers
    if layer.type() == QgsMapLayer.VectorLayer:
      if layer.providerType() not in ["ogr", "postgres"]:
        return (False, "Only ogr and postgres vector layers are supported now")
      if layer.providerType() == "ogr":
        if layer.storageType() != "ESRI Shapefile":
          return (False, "Only 'ESRI Shapefile' ogr provider is supported now!")
      if layer.providerType() == "postgres":
        if NO_PSYCOPG2:
          return (False, "psycopg2 libraries are not installed")
        if not PostgresMetadataProvider.checkExtension(layer.source()):
          if not PostgresMetadataProvider.installExtension(layer.source()):
            return (False, "MetadataPostgis extension are not installed for this DB or connection has failed.")

    # layer is supported
    return (True, "Layer is supported")

  @staticmethod
  def getProvider(layer):
      ok, msg = MetadataProvider.isLayerSupport(layer)
      if not ok:
          raise Exception(msg)

    # only file based rasters
      if layer.type() == QgsMapLayer.RasterLayer:
          return FileMetadataProvider(layer)

    # vectors
      if layer.providerType() == "ogr":
          return FileMetadataProvider(layer)

      if layer.providerType() == "postgres":
          return PostgresMetadataProvider(layer)

      return None

# Metadata provider based on files
class FileMetadataProvider(MetadataProvider):
  META_EXT = '.xml'

  def __init__(self, layer):
    if type(layer) == type(unicode()):
      self.layerFilePath = layer
    else:
      self.layerFilePath = unicode(layer.source())
    self.metaFilePath = self.layerFilePath + self.META_EXT

  def checkExists(self):
    # TODO: Add content check on empty
    return path.exists(self.metaFilePath)

  def getMetadata(self):
    #read metadata from file
    metaFile = codecs.open(self.metaFilePath, "r", encoding="utf-8")
    content = metaFile.read()
    metaFile.close()
    return content

  def setMetadata(self, metadata):
    metaFile = codecs.open(self.metaFilePath, "w", encoding="utf-8")
    metaFile.write(metadata)
    metaFile.close()

# Metadata provider based on FS DB
class LocalDbMetadataProvider(MetadataProvider):
  pass

# Abstract metadata provider for remoute DB
class RemoteDbMetadataProvider(MetadataProvider):
  def __init__(self, layer):
    self.uri = layer.source()
    self.dsURI = QgsDataSourceURI(self.uri)


# Metadata provider for postgresql
class PostgresMetadataProvider(RemoteDbMetadataProvider):
  def checkExists(self):
    if self.getMetadata():
      return True
    else:
      return False

  def getMetadata(self):
    conn = psycopg2.connect(str(self.dsURI.connectionInfo()))
    cur = conn.cursor()
    cur.callproc("GetIsoMetadata", [str(self.dsURI.schema()), str(self.dsURI.table())])
    res = cur.fetchone()
    if res is None or res[0] is None:
        metadata = ''
    else:
        metadata = res[0]
    cur.close()
    conn.close()
    return metadata

  def setMetadata(self, metadata):
    conn = psycopg2.connect(str(self.dsURI.connectionInfo()))
    cur = conn.cursor()
    cur.callproc("RegisterIsoMetadata", [str(self.dsURI.schema()), str(self.dsURI.table()), metadata])
    conn.commit()
    cur.close()
    conn.close()

  @staticmethod
  def checkExtension(uri):
    dsUri = QgsDataSourceURI(uri)
    try:
      conn = psycopg2.connect(str(dsUri.connectionInfo()))
      cur = conn.cursor()
      cur.execute("SELECT COUNT(*) FROM pg_class WHERE relname='iso_metadata'")
      tableCount = cur.fetchone()[0]
      cur.close()
      conn.close()
      return (tableCount == 1)
    except:
      return False

  @staticmethod
  def installExtension(uri):
    dsUri = QgsDataSourceURI(uri)
    try:
      file = (path.join(path.abspath(path.dirname(__file__)), 'postgresql_ext/extension.sql'))
      procedures  = open(file,'r').read()
      conn = psycopg2.connect(str(dsUri.connectionInfo()))
      cur = conn.cursor()
      cur.execute(procedures)
      conn.commit()
      cur.close()
      conn.close()
      return True
    except psycopg2.DatabaseError, e:
      print "Exception executing sql: ", e
      return False
