from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from qgis.core import *
from geoserver.layergroup import LayerGroup, UnsavedLayerGroup
from opengeo.qgis import layers as qgislayers
from opengeo.qgis.catalog import OGCatalog, createPGFeatureStore
from opengeo.gui.qgsexploreritems import QgsStyleItem
from opengeo.gui.gsnameutils import xmlNameFixUp, xmlNameIsValid, xmlNameRegex
from opengeo.qgis.utils import UserCanceledOperation
from opengeo.geoserver.util import groupsWithLayer, removeLayerFromGroups, \
    addLayerToGroups
from opengeo.gui.dialogs.gsnamedialog import getGSLayerName, getGSStyleName
from opengeo.gui.dialogs.groupdialog import PublishLayerGroupDialog


def noDefaultStyleError(explorer, layername):
    explorer.setError(
        "Generated layer '{0}' does not have an assigned default style. "
        "Without one, some Geoserver operations may fail, "
        "like OWS capabilities requests.".format(layername))


def publishDraggedGroup(explorer, groupItem, catalog, workspace=None):
    groupname = groupItem.element
    groups = qgislayers.getGroups()
    grouplyrs = groups[groupname]

    overwrite = bool(QSettings().value(
        "/OpenGeo/Settings/GeoServer/OverwriteGroupLayers", True, bool))
    try:
        dlg = PublishLayerGroupDialog(catalog, groupname, grouplyrs,
                                      workspace=workspace,
                                      overwritegroup=True,
                                      overwritelayers=overwrite)
        dlg.exec_()
    except UserCanceledOperation:
        return False
    grpName = dlg.definedname
    toPublish = dlg.topublish
    if grpName is None:  # toPublish can be empty list
        return False
    catgroup = catalog.get_layergroup(grpName)

    names = []
    if toPublish:
        explorer.setProgressMaximum(len(toPublish), "Publish layers")
        progress = 0
        layernames = []
        for layer, catalog, workspc, layername in toPublish:
            layernames.append(layername)
            explorer.setProgress(progress)
            ogcat = OGCatalog(catalog)
            if not explorer.run(ogcat.publishLayer,
                                None,
                                [],
                                layer, workspc, True, layername):
                explorer.setProgress(0)
                return
            progress += 1
            explorer.setProgress(progress)
        explorer.resetActivity()
        names = reversed(layernames)

    if catgroup:
        catalog.delete(catgroup)

    #TODO calculate bounds
    bbox = None
    group = UnsavedLayerGroup(catalog, grpName, names, names, bbox)

    return explorer.run(catalog.save,
                        "Create layer group from group '" + groupname + "'",
                        [],
                        group)


def publishDraggedLayer(explorer, layer, workspace):
    cat = workspace.catalog
    ogcat = OGCatalog(cat)
    gslayers = [lyr.name for lyr in cat.get_layers()]
    layername = layer.name()
    if qgislayers.isPostGisLayer(layer):
        layername += "_table"
    try:
        lyrname = getGSLayerName(name=xmlNameFixUp(layername),
                                 names=gslayers,
                                 unique=False)
    except UserCanceledOperation:
        return False

    return explorer.run(ogcat.publishLayer,
                        "Publish layer from layer '" + lyrname + "'",
                        [],
                        layer, workspace, True, lyrname)


def publishDraggedTable(tree, explorer, table, workspace):
    if not xmlNameIsValid(table.name, xmlNameRegex()):
        QtGui.QMessageBox.warning(explorer, "Invalid name",
                                  ("The table name (%s) is not a valid XML name.\n"
                                  + "This could cause problems when published to GeoServer.\n"
                                  + "Please rename it and retry publishing.") % table.name)
        return False
    cat = workspace.catalog
    if int(table.srid) == 0:
        explorer.setWarning("PostGIS table '{0}' has no SRID; ESPG:4326 will "
                            "be assigned.".format(table.name))

    gslayers = [lyr.name for lyr in cat.get_layers()]
    try:
        lyrname = getGSLayerName(name=xmlNameFixUp(table.name + "_table"),
                                 names=gslayers,
                                 unique=False)
    except UserCanceledOperation:
        return False

    catItem = tree.findFirstItem(cat)
    toUpdate = [catItem.layersItem]
    res = explorer.run(publishTable,
                       "Publish table from table '" + table.name + "'",
                       toUpdate,
                       table, cat, workspace, True, lyrname)
    if res:
        # add existing style to layer, or later some operations may fail,
        # like malformed XML when getting capabilities for OWS connections
        pglyr = cat.get_layer(lyrname)
        pgitem = tree.findFirstItem(pglyr)
        if pgitem is None:
            print "pgitem not found"
            return False
        if not pgitem.addStyleToLayer(explorer):  # handles refresh of item
            # user cancelled AddStyleToLayerDialog
            noDefaultStyleError(explorer, lyrname)
            return False
        else:
            catItem.layersItem.refreshContent(explorer)
    return res


def publishTable(table, catalog = None, workspace = None, overwrite=True,
                 name=None, storename=None):
    if catalog is None:
        pass

    lyrname = xmlNameFixUp(name)  # usually fixed up by now

    # check for table.name conflict in existing layer names where the table.name
    # is not the same as the user-chosen layer name, i.e. unintended overwrite
    resource = catalog.get_resource(table.name)
    if resource is not None and table.name != lyrname:
        raise Exception("PostGIS table name conflicts with "
                        "existing GeoServer layer name: {0}\n"
                        "You may need to rename GeoServer layer name."
                        .format(table.name))

    workspace = workspace if workspace is not None else catalog.get_default_workspace()
    connection = table.conn
    geodb = connection.geodb
    conname = "{0}_{1}".format(connection.name, table.schema)
    storename = xmlNameFixUp(storename or conname)

    if not xmlNameIsValid(storename):
        raise Exception("Database connection name is invalid XML and can "
                        "not be auto-fixed: {0} -> {1}"
                        .format(conname, storename))

    if not geodb.user:
        raise Exception("GeoServer requires database connection's username "
                        "to be defined")

    store = createPGFeatureStore(catalog,
                         storename,
                         workspace = workspace,
                         overwrite = True,
                         host = geodb.host,
                         database = geodb.dbname,
                         schema = table.schema,
                         port = geodb.port,
                         user = geodb.user,
                         passwd = geodb.passwd)
    if store is not None:
        rscname = name if table.name != name else table.name
        grpswlyr = []
        if overwrite:
            # See notes about possible issues in OGCatalog._publishExisting()
            flyr = catalog.get_layer(rscname)
            if flyr is not None:
                grpswlyr = groupsWithLayer(catalog, flyr)
                if grpswlyr:
                    removeLayerFromGroups(catalog, flyr, grpswlyr)
                catalog.delete(flyr)

            frsc = store.get_resources(name=rscname)
            if frsc is not None:
                catalog.delete(frsc)

        epsg = table.srid if int(table.srid) != 0 else 4326
        ftype = catalog.publish_featuretype(table.name, store,
                                            "EPSG:" + str(epsg))
        # once table-based layer created, switch name to user-chosen
        if table.name != rscname:
            ftype.dirty["name"] = rscname
            ftype.dirty["title"] = rscname
            catalog.save(ftype)

        if overwrite and grpswlyr:
            ftype = catalog.get_resource(rscname)
            if ftype:
                addLayerToGroups(catalog, ftype, grpswlyr, workspace=workspace)


def publishDraggedStyle(explorer, layerName, catalogItem, name=None):
    catalog = catalogItem.element
    ogcat = OGCatalog(catalog)
    toUpdate = [catalogItem.stylesItem]
    if name is not None:
        stylename = name
    else:
        styles = [style.name for style in catalog.get_styles()]
        try:
            stylename = getGSStyleName(name=xmlNameFixUp(layerName),
                                       names=styles,
                                       unique=False)
        except UserCanceledOperation:
            return False
    return explorer.run(ogcat.publishStyle,
                        "Publish style from layer '" + layerName + "'",
                        toUpdate,
                        layerName, True, stylename)

def addDraggedLayerToGroup(explorer, layer, groupItem):
    group = groupItem.element
    styles = group.styles
    layers = group.layers
    if layer.name not in layers:
        layers.append(layer.name)
        styles.append(layer.default_style.name)
    group.dirty.update(layers = layers, styles = styles)
    explorer.run(layer.catalog.save,
                 "Update group '" + group.name + "'",
                 [groupItem],
                 group)

def addDraggedStyleToLayer(tree, explorer, styleItem, layerItem):
    catalog = layerItem.element.catalog
    catItem = tree.findFirstItem(catalog)
    toUpdate = [catItem.layersItem]
    if isinstance(styleItem, QgsStyleItem):
        styleName = styleItem.element.name()  # = layer name
        styles = [style.name for style in catalog.get_styles()]
        try:
            stylname = getGSStyleName(name=xmlNameFixUp(styleName),
                                      names=styles,
                                      unique=False)
        except UserCanceledOperation:
            return False
        if not publishDraggedStyle(explorer, styleName, catItem,
                                   name=stylname):
            return False
        style = catalog.get_style(stylname)
        toUpdate.append(catItem.stylesItem)
    else:
        style = styleItem.element
    layer = layerItem.element

    if not hasattr(layer, "default_style") or layer.default_style is None:
        # if default style is missing, make dragged style the layer's default
        # without a default style, some GeoServer operations may fail
        layer.default_style = style
    else:
        # add to layer's additional styles
        styles = layer.styles
        styles.append(style)
        layer.styles = styles

    return explorer.run(
        catalog.save,
        "Add style '" + style.name + "' to layer '" + layer.name + "'",
        toUpdate,
        layer)


def addDraggedUrisToWorkspace(uris, catalog, workspace, explorer, tree):
    if uris:
        if len(uris) > 1:
            explorer.setProgressMaximum(len(uris))
        for i, uri in enumerate(uris):
            if isinstance(uri, basestring):
                layerName = QtCore.QFileInfo(uri).completeBaseName()
                layer = QgsRasterLayer(uri, layerName)
            else:
                layer = QgsRasterLayer(uri.uri, uri.name)
            if not layer.isValid() or layer.type() != QgsMapLayer.RasterLayer:
                if isinstance(uri, basestring):
                    layerName = QtCore.QFileInfo(uri).completeBaseName()
                    layer = QgsVectorLayer(uri, layerName, "ogr")
                else:
                    layer = QgsVectorLayer(uri.uri, uri.name, uri.providerKey)
                if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                    layer.deleteLater()
                    name = uri if isinstance(uri, basestring) else uri.uri
                    explorer.setError("Error reading file {} or it is not a valid layer file".format(name))
                else:
                    if not publishDraggedLayer(explorer, layer, workspace):
                        return []
            else:
                if not publishDraggedLayer(explorer, layer, workspace):
                    return []
            explorer.setProgress(i + 1)
        explorer.resetActivity()
        return [tree.findAllItems(catalog)[0]]
    else:
        return []
