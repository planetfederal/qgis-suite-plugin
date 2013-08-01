import os
from PyQt4 import QtGui, QtCore
from qgis.core import *
from opengeo.postgis.connection import PgConnection
from opengeo.gui.exploreritems import TreeItem
from opengeo.gui.layerdialog import PublishLayerDialog
from opengeo.qgis.catalog import OGCatalog
from opengeo.postgis.postgis_utils import tableUri

pgIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/pg.png")   
 
class PgConnectionsItem(TreeItem):

    def __init__(self):             
        TreeItem.__init__(self, None, pgIcon, "PostGIS connections") 
        
    def populate(self):        
        settings = QtCore.QSettings()
        settings.beginGroup(u'/PostgreSQL/connections')
        for name in settings.childGroups():
            try:
                settings.beginGroup(name)                
                conn = PgConnection(name, settings.value('host'), int(settings.value('port')), 
                                settings.value('database'), settings.value('username'), 
                                settings.value('password'))                 
                item = PgConnectionItem(conn)              
                item.populate()
                self.addChild(item)
            except Exception, e:
                #if there is a problem connecting, we do not add the item
                pass                      
        settings.endGroup()            
                  
class PgConnectionItem(TreeItem): 
    def __init__(self, conn):                      
        TreeItem.__init__(self, conn, pgIcon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)          
        
    def populate(self):
        schemas = self.element.schemas()
        for schema in schemas:
            schemItem = PgSchemaItem(schema)
            schemItem.populate()
            self.addChild(schemItem)
            
    def contextMenuActions(self, explorer):
        self.explorer = explorer          
        newSchemaAction = QtGui.QAction("New schema...", explorer)
        newSchemaAction.triggered.connect(self.newSchema) 
        sqlAction = QtGui.QAction("Run SQL...", explorer)
        sqlAction.triggered.connect(self.runSql)                                           
        return [newSchemaAction]
                
    def runSql(self):
        pass
    
    def newSchema(self):
        pass 
                    
class PgSchemaItem(TreeItem): 
    def __init__(self, schema): 
        pgIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/namespace.png")                        
        TreeItem.__init__(self, schema, pgIcon)
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled)
        
    def populate(self):
        tables = self.element.tables()
        for table in tables:
            tableItem = PgTableItem(table)            
            self.addChild(tableItem)      

    def contextMenuActions(self, explorer):        
        self.explorer = explorer           
        newTableIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/new_table.png")                         
        newTableAction = QtGui.QAction(newTableIcon, "New table...", explorer)
        newTableAction.triggered.connect(self.newTable)                                                                  
        deleteAction= QtGui.QAction("Delete", explorer)
        deleteAction.triggered.connect(self.deleteSchema)  
        renameAction= QtGui.QAction("Rename...", explorer)
        renameAction.triggered.connect(self.renameSchema)
        return [newTableAction, deleteAction, renameAction]
        
    def deleteSchema(self):
        self.explorer.run(self.element.conn.geodb.delete_schema, 
                          "Schema " + self.element.name + " correctly deleted",
                          [self.parent()], 
                          self.element.name)
    
    def renameSchema(self):
        text, ok = QtGui.QInputDialog.getText(self.explorer, "Schema name", "Enter new name for schema", text="schema")
        if ok:
            self.explorer.run(self.element.conn.geodb.rename_schema, 
                          "Schema " + self.element.name + " correctly renamed to " + text,
                          [self.parent()], 
                          self.element.name, text)      
    
    def newTable(self):
        pass                    
        
class PgTableItem(TreeItem): 
    def __init__(self, table):                               
        TreeItem.__init__(self, table, self.getIcon(table))
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled)
        
    def getIcon(self, table):        
        tableIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/table.png")
        viewIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/view.png")
        layerPointIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer_point.png")
        layerLineIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer_line.png")
        layerPolygonIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer_polygon.png")        
        layerUnknownIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../images/layer_unknown.png")
            
        if table.geomtype is not None:        
            if table.geomtype.find('POINT') != -1:
                return layerPointIcon
            elif table.geomtype.find('LINESTRING') != -1:
                return layerLineIcon
            elif table.geomtype.find('POLYGON') != -1:
                return layerPolygonIcon
            return layerUnknownIcon        

        if table.isView:
            return viewIcon
        
        return tableIcon
    
    def contextMenuActions(self, explorer):
        self.explorer = explorer  
        publishPgTableAction = QtGui.QAction("Publish...", explorer)
        publishPgTableAction.triggered.connect(self.publishPgTable)            
        publishPgTableAction.setEnabled(len(explorer.tree.gsItem.catalogs()) > 0)
        importAction = QtGui.QAction("Import file/layer...", explorer)
        importAction.triggered.connect(self.importIntoTable)                    
        exportAction= QtGui.QAction("Export...", explorer)
        exportAction.triggered.connect(self.exportTable)    
        editAction= QtGui.QAction("Edit...", explorer)
        editAction.triggered.connect(self.editTable)   
        deleteAction= QtGui.QAction("Delete", explorer)
        deleteAction.triggered.connect(self.deleteTable)  
        renameAction= QtGui.QAction("Rename...", explorer)
        renameAction.triggered.connect(self.renameTable)                 
        vacuumAction= QtGui.QAction("Vacuum analyze", explorer)
        vacuumAction.triggered.connect(self.vacuumTable)
        return [publishPgTableAction, importAction, exportAction, editAction, deleteAction, renameAction, vacuumAction]
        
    def importIntoTable(self):
        pass
    
    def exportTable(self):
        table = self.element
        uri = tableUri(table)
        layer = QgsVectorLayer(uri, self.element.name, "postgres")

        from db_manager.dlg_export_vector import DlgExportVector
        dlg = DlgExportVector(layer, None, self.explorer)
        dlg.exec_()

        layer.deleteLater()

    
    def editTable(self):
        pass
    
    def vacuumTable(self):
        self.explorer.run(self.element.conn.geodb.vacuum_analize, 
                  "Table " + self.element.name + " correctly vacuumed",
                  [self.parent()], 
                  self.element.name, self.element.schema.name)
    
    def deleteTable(self):
        self.explorer.run(self.element.conn.geodb.delete_table, 
                          "Table " + self.element.name + " correctly deleted",
                          [self.parent()], 
                          self.element.name)
    
    def renameTable(self):
        text, ok = QtGui.QInputDialog.getText(self.explorer, "Table name", "Enter new name for table", text="table")
        if ok:
            self.explorer.run(self.element.conn.geodb.rename_table, 
                          "Table " + self.element.name + " correctly renamed to " + text,
                          [self.parent()], 
                          self.element.name, text, self.element.schema.name)      
    
    
    def publishPgTable(self):
        dlg = PublishLayerDialog(self.explorer.tree.gsItem.catalogs())
        dlg.exec_()      
        if dlg.catalog is None:
            return
        cat = dlg.catalog          
        catItem = self.explorer.tree.findAllItems(cat)[0]
        toUpdate = [catItem]                    
        self.explorer.run(self._publishTable,
                 "Layer correctly published from layer '" + self.element.name() + "'",
                 toUpdate,
                 self.element, cat, dlg.workspace)
        
                
    def _publishTable(self, table, catalog = None, workspace = None):
        if catalog is None:
            pass       
        workspace = workspace if workspace is not None else catalog.get_default_workspace()        
        connection = table.conn 
        geodb = connection.geodb      
        catalog.create_pg_featurestore(connection.name,                                           
                                           workspace = workspace,
                                           overwrite = True,
                                           host = geodb.host,
                                           database = geodb.dbname,
                                           schema = table.schema,
                                           port = geodb.port,
                                           user = geodb.user,
                                           passwd = geodb.passwd)
        catalog.create_pg_featuretype(table.name, connection.name, workspace)  
