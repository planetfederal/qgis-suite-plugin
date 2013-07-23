from opengeo.postgis.postgis_utils import GeoDB
from opengeo.postgis.schema import Schema

class PgConnection(object):       
    
    def __init__(self, name, host, port, database, username, password):
        self.name = name
        self.conn = GeoDB(host, port, database, username, password)
        
    def schemas(self):
        schemas = self.conn.list_schemas()
        return [Schema(self.conn, name) for oid, name, owner, perms in schemas]        
        
