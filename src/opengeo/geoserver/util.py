from zipfile import ZipFile
import tempfile
from os import path

def shapefile_and_friends(path):
    return dict((ext, path + "." + ext) for ext in ['shx', 'shp', 'dbf', 'prj'])

_shp_exts = ["dbf","prj","shx"]
_shp_exts = _shp_exts + map(lambda s: s.upper(), _shp_exts)

def shp_files(fpath):
    basename, ext = path.splitext(fpath)
    paths = [ "%s.%s" % (basename,ext) for ext in _shp_exts ]
    paths.append(fpath)
    return filter(lambda f: path.exists(f),  paths)
    
def create_zip(fpaths):
    _,payload = tempfile.mkstemp(suffix='.zip')
    zipf = ZipFile(payload, "w")
    for fp in fpaths:
        basename = path.basename(fp)
        zipf.write(fp, basename)
    zipf.close()
    return payload

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

def getLayerFromStyle(style):
    '''Tries to find out which layer is using a given style.
    Returns none if cannot find a layer using the style'''
    cat = style.catalog
    layers = cat.get_layers()
    for layer in layers:
        if layer.default_style.name == style.name:
            return layer
        alternateStyles = layer.styles
        for alternateStyle in alternateStyles:
            if style.name == alternateStyle.name:
                return layer

def groupsWithLayer(catalog, layer):
    grps = catalog.get_layergroups()
    grpswlyr = []
    for grp in grps:
        lyrs = grp.layers
        if lyrs is None:
            continue
        for lyr in lyrs:
            if layer.name == lyr:
                grpswlyr.append(grp)
                break
    return grpswlyr

def removeLayerFromGroups(catalog, layer, groups=None):
    grps = groups or catalog.get_layergroups()
    for grp in grps:
        lyrs = grp.layers
        if lyrs is None:
            continue
        if layer.name not in lyrs:
            continue
        styles = grp.styles
        idx = lyrs.index(layer.name)
        del lyrs[idx]
        del styles[idx]
        grp.dirty.update(layers=lyrs, styles=styles)
        catalog.save(grp)

def addLayerToGroups(catalog, layer, groups, workspace=None):
    '''This assumes the layer style with same name as layer already exists,
    otherwise None is assigned'''
    for grp in groups:
        lyrs = grp.layers
        styles = grp.styles
        lyrs.append(layer.name)
        style = catalog.get_style(layer.name, workspace=workspace)
        styles.append(style)
        grp.dirty.update(layers=lyrs, styles=styles)
        catalog.save(grp)
