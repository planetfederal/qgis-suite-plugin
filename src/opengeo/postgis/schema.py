from opengeo.postgis.table import Table

class Schema(object):
    
    def __init__(self, conn, name):
        self.name = name
        self.conn = conn
        
    def tables(self):
        tables = self.conn.geodb.list_geotables(self.name)   
        return [Table(self.conn, self.name, table[0], table[2], table[7]) for table in tables]
    
