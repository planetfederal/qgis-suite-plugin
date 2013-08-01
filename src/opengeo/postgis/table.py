class Table(object):
    
    
    def __init__(self, connection, schema, name, tabletype, geomtype):
        self.name = name
        self.tabletype = tabletype
        self.geomtype = geomtype
        self.schema = schema
        self.conn = connection
        self.isView = self.tabletype == u'v'
        
