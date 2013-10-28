import os
from opengeo.geoserver.util import shapefile_and_friends

PREFIX = "qgis_plugin_test_"

def safeName(name):
    return PREFIX + name

PT1 = safeName("pt1")
PT1JSON = safeName("pt1json")
PT2 = safeName("pt2")
PT3 = safeName("pt3")
DEM = safeName("dem")
DEMASCII = safeName("demascii")
GEOLOGY_GROUP = safeName("geology_landuse")
GEOFORMS = safeName("geoforms")
LANDUSE = safeName("landuse")
GROUP = safeName("group")
STYLE = safeName("style")
HOOK = safeName("hook")
WORKSPACE = safeName("workspace")
WORKSPACEB = safeName("workspaceb")

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
        
    for wsName in [WORKSPACE, WORKSPACEB]:
        ws = cat.get_workspace(wsName)
        if ws is not None:
            for store in cat.get_stores(ws):
                for resource in store.get_resources():
                    cat.delete(resource)
                cat.delete(store)    
            cat.delete(ws)
            ws = cat.get_workspace(wsName)    
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
    

