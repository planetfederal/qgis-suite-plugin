from postgis_utils import GeoDB
from schema import Schema
from qgis.core import *
from PyQt4 import QtCore

class PgConnection(object):       
    
    def __init__(self, name, host, port, database, username, password):
        self.name = name  
        self.host = host
        self.port = port
        self.database = database      
        try:
            self.geodb = GeoDB(host, port, database, username, password)
            self.isValid = True
        except:
            self.isValid = False
        
        
    def schemas(self):
        schemas = self.geodb.list_schemas()
        return [Schema(self, name) for oid, name, owner, perms in schemas]        
        
    def reconnect(self, username, password):
        try:
            self.geodb =  GeoDB(self.host, self.port, self.database, username, password)
            self.isValid = True
        except:
            self.isValid = False
            
            
    def importFileOrLayer(self, source, schema, tablename, overwrite):
    
        pk = "id"
        geom = "geom" 
        providerName = "postgres" 
        
        if isinstance(source, basestring):
            layerName = QtCore.QFileInfo(source).completeBaseName()
        else:
            layerName = source.name()
        
        if tablename is None:
            tablename = layerName
    
        uri = QgsDataSourceURI()    
        uri.setConnection(self.geodb.host, str(self.geodb.port), self.geodb.dbname, self.geodb.user, self.geodb.passwd)    
        uri.setDataSource(schema, tablename, geom, "", pk)
    
        options = {}
        if overwrite:
            options['overwrite'] = True
        else:
            options['append'] = True
            
        if isinstance(source, basestring):
            layer = QgsVectorLayer(source, layerName, "ogr")    
            if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                layer.deleteLater()
                raise WrongLayerFileError("Error reading file {} or it is not a valid vector layer file".format(source))
        else:
            layer = source
    
        ret, errMsg = QgsVectorLayerImport.importLayer(layer, uri.uri(), providerName, layer.crs(), False, False, options)
        if ret != 0:
            raise Exception(errMsg) 
        
    
class WrongLayerFileError(Exception):
    pass                   