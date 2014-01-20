import os
from opengeo.geoserver.util import shapefile_and_friends
from opengeo.postgis.connection import PgConnection
from opengeo.postgis.schema import Schema


PREFIX = "qgis_plugin_test_"

def safeName(name):
    return PREFIX + name

PT1 = safeName("pt1")
PT1JSON = safeName("pt1json")
PT2 = safeName("pt2")
PT3 = safeName("pt3")
DEM = safeName("dem")
DEM2 = safeName("dem2")
DEMASCII = safeName("demascii")
GEOLOGY_GROUP = safeName("geology_landuse")
GEOFORMS = safeName("geoforms")
LANDUSE = safeName("landuse")
GROUP = safeName("group")
STYLE = safeName("style")
HOOK = safeName("hook")
WORKSPACE = safeName("workspace")
WORKSPACEB = safeName("workspaceb")
PUBLIC_SCHEMA = "public"
OPENGEO_SCHEMA = safeName("opengeo")


def getPostgresConnection(name="connection"):
    conn = PgConnection(safeName(name), "localhost", 54321,
                        "opengeo", "postgres", "postgres")
    if not conn.isValid:
        conn = PgConnection(safeName(name), "localhost", 5432,
                        "opengeo", "postgres", "postgres")
    assert conn.isValid
    return conn


def cleanCatalog(cat):
       
    for groupName in [GROUP, GEOLOGY_GROUP]:
        group = cat.get_layergroup(groupName)
        if group is not None:
            cat.delete(group)
            group = cat.get_layergroup(groupName)
            assert group is None
        
    toDelete = []
    for layer in cat.get_layers():
        if layer.name.startswith(PREFIX):
            toDelete.append(layer)    
    for style in cat.get_styles():
        if style.name.startswith(PREFIX):
            toDelete.append(style)                            
    
    for e in toDelete:        
        cat.delete(e, purge = True)
        
    for ws in cat.get_workspaces():
        if not ws.name.startswith(PREFIX):
            continue
        if ws is not None:
            for store in cat.get_stores(ws):
                for resource in store.get_resources():
                    try:
                        cat.delete(resource)
                    except:
                        pass
                cat.delete(store)    
            cat.delete(ws)
            ws = cat.get_workspace(ws.name)
            assert ws is None        

    
def populateCatalog(cat):
    cleanCatalog(cat)
    cat.create_workspace(WORKSPACE, "http://test.com")
    ws = cat.get_workspace(WORKSPACE)
    path = os.path.join(os.path.dirname(__file__), "data", PT2)
    data = shapefile_and_friends(path)
    cat.create_shp_featurestore(PT2, data, ws)
    path = os.path.join(os.path.dirname(__file__), "data", PT3)
    data = shapefile_and_friends(path)
    cat.create_shp_featurestore(PT3, data, ws)
    sldfile = os.path.join(os.path.dirname(__file__), "resources", "vector.sld")
    with open(sldfile, 'r') as f:
        sld = f.read()
    cat.create_style(STYLE, sld, True)
    group = cat.create_layergroup(GROUP, [PT2])
    cat.save(group)
    cat.create_workspace(WORKSPACEB, "http://testb.com")
    cat.set_default_workspace(WORKSPACE)
    

def cleanDatabase(conn):    
    schema = Schema(conn, PUBLIC_SCHEMA)
    for table in schema.tables():
        if table.name.startswith(PREFIX):
            conn.geodb.delete_table(table.name, PUBLIC_SCHEMA)

