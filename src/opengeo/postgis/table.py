class Table(object):
    
    def __init__(self, connection, schema, name):
        self.name = name
        self.schema = schema
        self.connection = connection
