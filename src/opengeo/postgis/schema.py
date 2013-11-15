from opengeo.postgis.table import Table

class Schema(object):
    
    def __init__(self, conn, name):
        self.name = name
        self.conn = conn
        
    def tables(self):
        tables = self.conn.geodb.list_geotables(self.name) 
        blacklist = ['geometry_columns', 'geography_columns', 'spatial_ref_sys', 'raster_columns', 'raster_overviews']
        return [Table(self.conn, self.name, table[0], table[2], table[6], table[7], table[9]) 
                for table in tables if table[0] not in blacklist and table[6] is not None]
    
