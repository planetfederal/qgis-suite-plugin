from opengeo.postgis.postgis_utils import GeoDB

class Schema(object):
    
    def __init__(self, name, host, port, database, username, password):
        self.name = name
        self.conn = GeoDB(host, port, database, username, password)
        
    def table(self):
        schemas = self.conn.list_geotables()
        print schemas
        #return [Table(self.conn, name) for oid, name, owner, perms in schemas]
    
