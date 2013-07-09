# shapefile_and_friends = None
# shapefile_plus_sidecars = shapefile_and_friends("test/data/states")

def shapefile_and_friends(path):
    return dict((ext, path + "." + ext) for ext in ['shx', 'shp', 'dbf', 'prj'])

def name(named):
    """Get the name out of an object.  This varies based on the type of the input:
       * the "name" of a string is itself
       * the "name" of None is itself
       * the "name" of an object with a property named name is that property -
         as long as it's a string
       * otherwise, we raise a ValueError
    """
    if isinstance(named, basestring) or named is None:
        return named
    elif hasattr(named, 'name'):
        if isinstance(named.name, basestring):
            return named.name
        elif callable(named.name) and isinstance(named.name(), basestring):
            return named.name()    
    else:
        raise ValueError("Can't interpret %s as a name or a configuration object" % named)
    