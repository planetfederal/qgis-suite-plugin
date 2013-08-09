class Table(object):
    
    
    def __init__(self, connection, schema, name, tabletype, geomfield, geomtype, srid):
        self.name = name
        self.tabletype = tabletype
        self.geomfield = geomfield
        self.geomtype = geomtype
        self.schema = schema
        self.srid = srid
        self.conn = connection
        self.isView = self.tabletype == u'v'
        
