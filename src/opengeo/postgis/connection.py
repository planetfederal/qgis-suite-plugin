from opengeo.postgis.postgis_utils import GeoDB
from opengeo.postgis.schema import Schema

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