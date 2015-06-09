from postgis_utils import GeoDB
from schema import Schema
from qgis.core import *
from PyQt4 import QtCore
import re
import subprocess
import os

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

        if overwrite:
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
            options['overwrite'] = True
            if singleGeom:
                options['forceSinglePartGeometryType'] = True

            if isinstance(source, basestring):
                layer = QgsVectorLayer(source, layerName, "ogr")
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    layer.deleteLater()
                    raise WrongLayerFileError("Error reading file {} or it is not a valid vector layer file".format(source))
            else:
                layer = source
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    raise WrongLayerFileError("Layer '%s' is not valid or is not a vector layer".format(layer.name()))

            ret, errMsg = QgsVectorLayerImport.importLayer(layer, uri.uri(), providerName, layer.crs(), False, False, options)
            if ret != 0:
                raise Exception(errMsg)
        else:
            if isinstance(source, QgsMapLayer):
                source = source.source()

            args = ["shp2pgsql", "-a"]
            if singleGeom:
                args.append("-S")
            args.extend([source, schema + "." + tablename])
            if os.name == 'nt':
                cmdline = subprocess.list2cmdline(args)
                data = None

                p = os.popen3(cmdline)
                data = p[1].read()

                cursor = self.geodb.con.cursor()
                newcommand = re.compile(";$", re.MULTILINE)

                # split the commands
                cmds = newcommand.split(data)
                for cmd in cmds[:-1]:
                    # run SQL commands within current DB connection
                    self.geodb._exec_sql(cursor, cmd)
                data = cmds[-1]

                self.geodb.con.commit()

                if data is None or len(data) == 0:
                    raise Exception("".join(p[2].readlines()))
            else:
                # start shp2pgsql as subprocess
                p = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # read the output while the process is running
                data = ''
                cursor = self.geodb.con.cursor()
                newcommand = re.compile(";$", re.MULTILINE)
                while p.poll() == None:
                    data += p.stdout.read()

                    # split the commands
                    cmds = newcommand.split(data)
                    for cmd in cmds[:-1]:
                        # run SQL commands within current DB connection
                        self.geodb._exec_sql(cursor, cmd)
                    data = cmds[-1]

                # commit!
                self.db.con.commit()

                if p.returncode != 0:
                    raise Exception(p.stderr.readlines().join("\n"))


class WrongLayerFileError(Exception):
    pass