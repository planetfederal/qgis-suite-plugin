from postgis_utils import GeoDB
from schema import Schema
from qgis.core import *
from PyQt4 import QtCore
from opengeo.gui.dialogs.gsnamedialog import getPostGisTableName
from opengeo.gui.gsnameutils import xmlNameIsValid, xmlNameRegex


class PgConnection(object):

    def __init__(self, name, host, port, database, username, password):
        self.name = name
        self.host = host
        self.port = port
        self.database = database
        try:
            self.geodb = GeoDB(host, port, database, username, password)
            self.isValid = True
            self.username = username
            self.password = password
        except:
            self.isValid = False


    def schemas(self):
        schemas = self.geodb.list_schemas()
        return [Schema(self, name) for oid, name, owner, perms in schemas]

    def reconnect(self, username = None, password = None):
        try:
            self.geodb =  GeoDB(self.host, self.port, self.database, username or self.username, password or self.password)
            self.isValid = True
        except:
            self.isValid = False


    def importFileOrLayer(self, source, schema, tablename, overwrite, singleGeom = False):

        if isinstance(source, basestring):
            layerName = QtCore.QFileInfo(source).completeBaseName()
        else:
            layerName = source.name()

        if tablename is None:
            tablename = layerName

        if not xmlNameIsValid(tablename, xmlNameRegex()):
            tablename = getPostGisTableName(name=tablename, names=[], unique=False)

        if isinstance(source, basestring):
            layer = QgsVectorLayer(source, layerName, "ogr")
            if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                layer.deleteLater()
                raise WrongLayerFileError("Error reading file {} or it is not a valid vector layer file".format(source))
        else:
            layer = source
            if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                raise WrongLayerFileError("Layer '%s' is not valid or is not a vector layer".format(layer.name()))

        extent = '{},{},{},{}'.format(
                layer.extent().xMinimum(), layer.extent().xMaximum(),
                layer.extent().yMinimum(), layer.extent().yMaximum())
        geomtypes = {QGis.WKBPoint: 3,
                     QGis.WKBLineString: 4,
                     QGis.WKBPolygon: 5,
                     QGis.WKBMultiPoint: 7,
                     QGis.WKBMultiLineString: 9,
                     QGis.WKBMultiPolygon: 8}
        geomtype = geomtypes.get(layer.wkbType(), 0)
        import processing
        from processing.algs.gdal.ogr2ogrtopostgis import Ogr2OgrToPostGis as ogr2ogr
        params = {ogr2ogr.INPUT_LAYER: layer,
                    ogr2ogr.DBNAME: self.geodb.dbname,
                    ogr2ogr.PORT : self.geodb.port,
                    ogr2ogr.HOST : self.geodb.host,
                    ogr2ogr.USER : self.geodb.user,
                    ogr2ogr.PASSWORD: self.geodb.passwd,
                    ogr2ogr.SCHEMA: schema,
                    ogr2ogr.GTYPE: geomtype,
                    ogr2ogr.TABLE: tablename,
                    ogr2ogr.S_SRS: layer.crs().authid(),
                    ogr2ogr.T_SRS: layer.crs().authid(),
                    ogr2ogr.OVERWRITE: overwrite,
                    ogr2ogr.APPEND: not overwrite,
                    ogr2ogr.SPAT: extent
                    }
        processing.runalg("gdalogr:importvectorintopostgisdatabasenewconnection", params)

class WrongLayerFileError(Exception):
    pass