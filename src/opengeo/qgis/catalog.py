# -*- coding: utf-8 -*-

'''
Main functions for plugin functionality.
This is supposed to contain the functions to be called when using plugin 
functionality from the QGIS console.

It is basically a wrapper for a Catalog object, with some extra functionality 
and methods to interact with GIS objects
'''

import os
from qgis.core import *
from PyQt4.QtXml import *
from PyQt4.QtCore import *
from opengeo.qgis import layers, exporter, utils
from geoserver.catalog import ConflictingDataError, UploadError, FailedRequestError
from geoserver.catalog import Catalog as GSCatalog
from opengeo.qgis.sldadapter import adaptGsToQgs,\
    getGsCompatibleSld
from opengeo.qgis import uri as uri_utils
from opengeo.qgis.utils import tempFilename
from gsimporter.client import Client

try:
    from processing.modeler.ModelerAlgorithm import ModelerAlgorithm
    from processing.script.ScriptAlgorithm import ScriptAlgorithm
    from processing.parameters.ParameterRaster import ParameterRaster
    from processing.parameters.ParameterVector import ParameterVector
    from processing.outputs.OutputVector import OutputVector
    from processing.outputs.OutputRaster import OutputRaster
    from processing.gui.UnthreadedAlgorithmExecutor import UnthreadedAlgorithmExecutor
    from processing.core.SilentProgress import SilentProgress
    from processing.tools.dataobjects import getObjectFromUri as load
    from processing.modeler.Providers import Providers
    processingOk = True
except:
    processingOk = False
    
def createGeoServerCatalog(service_url = "http://localhost:8080/geoserver/rest", 
                 username="admin", password="geoserver", disable_ssl_certificate_validation=False):
    catalog = GSCatalog(service_url, username, password, disable_ssl_certificate_validation)
    return OGCatalog(catalog)
    

class OGCatalog(object):
    '''
    This class is a wrapper for a catalog object, with convenience methods to use it with QGIS layers
    '''
    
    def __init__(self, catalog):
        self.catalog = catalog
        #we also create a Client object pointing to the same url        
        self.client = Client(str(catalog.service_url), catalog.username, catalog.password)
        
    def clean(self):
        self.cleanUnusedStyles()
        self.cleanUnusedResources()
        
    def cleanUnusedStyles(self):
        '''cleans styles that are not used by any layer'''
        usedStyles = set()
        styles = self.catalog.get_styles()
        layers = self.catalog.get_layers()        
        for layer in layers:
            usedStyles.add(layer.default_style.name)
            usedStyles.update([s.name for s in layer.styles if s is not None])
                
        toDelete = [s for s in styles if s.name not in usedStyles]         
        for style in toDelete:            
            style.catalog.delete(style, purge = True)   
            
    def cleanUnusedResources(self):
        '''cleans resources that are not published through any layer in the catalog'''
        usedResources = set()
        resources = self.catalog.get_resources()
        layers = self.catalog.get_layers()        
        for layer in layers:
            usedResources.add(layer.resource.name)
            
        toDelete = [r for r in resources if r.name not in usedResources]         
        for resource in toDelete:                      
            resource.catalog.delete(resource)
            
        for store in self.catalog.get_stores():
            if len(store.get_resources()) == 0:
                self.catalog.delete(store)
                
    def consolidateStyles(self):
        '''
        Deletes styles that are redundant and just keeps one copy of them 
        in the catalog, configuring the corresponding layers to use that copy
        '''
        used = {}
        allstyles = self.catalog.get_styles()
        for style in allstyles:
            sld = style.sld_body.replace("<sld:Name>%s</sld:Name>" % style.name, "")
            if sld in used.keys():
                used[sld].append(style)
            else:
                used[sld] = [style]                        
                
        for sld, styles in used.iteritems():            
            if len(styles) == 1:
                continue
            #find the layers that use any of the secondary styles in the list, and make them use the first one
            styleNames = [s.name for s in styles[1:]]
            layers = self.catalog.get_layers()
            for layer in layers:  
                changed = False                              
                if layer.default_style.name in styleNames:
                    layer.default_style = styles[0]
                    changed = True                    
                alternateStyles = layer.styles
                newAlternateStyles = set()
                for alternateStyle in alternateStyles:                    
                    if alternateStyle.name in styleNames:
                        newAlternateStyles.add(styles[0])
                    else:
                        newAlternateStyles.add(alternateStyle)
                newAlternateStyles = list(newAlternateStyles)
                if newAlternateStyles != alternateStyles:
                    layer.styles = newAlternateStyles
                    changed = True                    
                if changed:
                    self.catalog.save(layer) 
                        
        
        

    
    def publishStyle(self, layer, overwrite = True, name = None):
        '''
        Publishes the style of a given layer style in the specified catalog. If the overwrite parameter is True, 
        it will overwrite a style with that name in case it exists
        '''        
        
        if isinstance(layer, basestring):
            layer = layers.resolveLayer(layer)         
        sld = getGsCompatibleSld(layer) 
        if sld is not None:       
            name = name if name is not None else layer.name()
            name = name.replace(" ", "_")            
            self.catalog.create_style(name, sld, overwrite)
        return sld
       
    def getDataFromLayer(self, layer):
        '''
        Returns the data corresponding to a given layer, ready to be passed to the
        method in the Catalog class for uploading to the server.
        If needed, it performs an export to ensure that the file format is supported 
        by the upload API to be used for import. In that case, the data returned
        will point to the exported copy of the data, not the original data source
        '''
        if layer.type() == layer.RasterLayer:
            data = exporter.exportRasterLayer(layer)                              
        else:      
            filename = exporter.exportVectorLayer(layer)        
            basename, extension = os.path.splitext(filename)        
            data = {
                'shp': basename + '.shp',
                'shx': basename + '.shx',
                'dbf': basename + '.dbf',
                'prj': basename + '.prj'
            }
        return data

    
    def _publishExisting(self, layer, workspace, overwrite):
        connName = self.getConnectionNameFromLayer(layer)
        uri = QgsDataSourceURI(provider.dataSourceUri())                                                                     
        store = createPGFeatureStore(self.catalog,
                                     connName,
                                     workspace = workspace,
                                     overwrite = overwrite,
                                     host = uri.host(),
                                     database = uri.database(),
                                     schema = uri.schema(),
                                     port = uri.port(),
                                     user = uri.username(),
                                     passwd = uri.password())
        self.catalog.publish_feature(uri.table(), store, layer.crs().authid())


    def _uploadRest(self, layer, workspace, overwrite, name):
        if layer.type() == layer.RasterLayer:
            path = self.getDataFromLayer(layer)
            self.catalog.create_coveragestore(name,
                                      path,
                                      workspace=workspace,
                                      overwrite=overwrite)
        elif layer.type() == layer.VectorLayer:
            path = self.getDataFromLayer(layer)
            self.catalog.create_featurestore(name,
                              path,
                              workspace=workspace,
                              overwrite=overwrite)


    def _uploadImporter(self, layer, workspace, overwrite, name):
        # @todo - more richness needed to allow ingestion into target store
        # versus just publishing the layer to a workspace as a shapefile
        path = self.getDataFromLayer(layer)
        if isinstance(path, dict):
            if 'shp' in path:
                path = path['shp']
            else:
                raise Exception('Unexpected condition : %s', path.keys())
        session = self.client.upload(path)
        if not session.tasks:
            raise Exception('Geoserver is not able to process the uploaded data')
        if len(session.tasks) != 1:
            # this probably shouldn't happen but just in case
            raise Exception('Unexpected condition')
        # set workspace if needed (network trip)
        # limitation in setting name as importer interprets this as a request
        # to use an existing store by name
        if workspace:
            session.tasks[0].set_target(workspace=workspace.name)
        if overwrite:
            session.tasks[0].set_update_mode('REPLACE')
        session.commit()


    def upload(self, layer, workspace=None, overwrite=True, name=None):        
        '''uploads the specified layer'''  

        if isinstance(layer, basestring):
            layer = layers.resolveLayer(layer)     

        name = name if name is not None else layer.name()
        title = name
        name = name.replace(" ", "_")

        settings = QSettings()
        restApi = bool(settings.value("/OpenGeo/Settings/GeoServer/UseRestApi", True, bool))

        if layer.type() not in (layer.RasterLayer, layer.VectorLayer):
            msg = layer.name() + ' is not a valid raster or vector layer'
            raise Exception(msg)

        provider = layer.dataProvider()
        try:
            if provider.name() == 'postgres':
                self._publishExisting(layer, workspace, overwrite)
            elif restApi:
                self._uploadRest(layer, workspace, overwrite, name)
            else:
                self._uploadImporter(layer, workspace, overwrite, name)
        except UploadError, e:
            msg = ('Could not save the layer %s, there was an upload '
                   'error: %s' % (layer.name(), str(e)))
            e.args = (msg,)
            raise
        except ConflictingDataError, e:
            # A datastore of this name already exists
            msg = ('GeoServer reported a conflict creating a store with name %s: '
                   '"%s". This should never happen because a brand new name '
                   'should have been generated. But since it happened, '
                   'try renaming the file or deleting the store in '
                   'GeoServer.' % (layer.name(), str(e)))
            e.args = (msg,)
            raise e
    
    
        # Verify the resource was created
        resource = self.catalog.get_resource(name)
        if resource is not None:
            assert resource.name == name
        else:
            msg = ('could not create layer %s.' % name)
            raise Exception(msg)
        
        if title != name:
            resource.dirty["title"] = title
            self.catalog.save(resource)
        if resource.latlon_bbox is None:
            box = resource.native_bbox[:4]
            minx, maxx, miny, maxy = [float(a) for a in box]
            if -180 <= minx <= 180 and -180 <= maxx <= 180 and \
                    -90 <= miny <= 90 and -90 <= maxy <= 90:
                resource.latlon_bbox = resource.native_bbox
                resource.projection = "EPSG:4326"
                self.catalog.save(resource)
            else:
                msg = ('Could not set projection for layer '
                       '[%s]. the layer has been created, but its projection should be set manually.')
                raise Exception(msg % layer.name())
            
    def getConnectionNameFromLayer(self, layer):
        connName = "postgis_store"
        uri = QgsDataSourceURI(layer.dataProvider().dataSourceUri())                
        host = uri.host()
        database = uri.database()
        port = uri.port()                
        settings = QSettings()
        settings.beginGroup(u'/PostgreSQL/connections')
        for name in settings.childGroups():
            settings.beginGroup(name)
            host2 = str(settings.value('host'))
            database2 = str(settings.value('database'))
            port2 = str(settings.value('port'))
            settings.endGroup()
            if port == port2 and database == database2 and host == host2:
                connName = name + "_" + str(uri.schema()) 
        settings.endGroup()
        return connName  
              
    def publishGroup(self, name, destName = None, workspace = None, overwrite = False, overwriteLayers = False):
        
        ''' 
        Publishes a group in the given catalog
        
        name: the name of the QGIS group to publish. It will also be used as the GeoServer layergroup name
        
        workspace: The workspace to add the group to
        
        overwrite: if True, it will overwrite a previous group with the specified name, if it exists
        
        overwriteLayers: if False, in case a layer in the group is not found in the specified workspace, the corresponding layer
        from the current QGIS project will be published, but all layers of the group that can be found in the GeoServer
        workspace will not be published. If True, all layers in the group are published, even if layers with the same name 
        exist in the workspace
        '''
                
        groups = layers.getGroups()
        if name not in groups:
            raise Exception("The specified group does not exist")
        
        destName = destName if destName is not None else name
        gsgroup = self.catalog.get_layergroup(destName)
        if gsgroup is not None and not overwrite:
            return
        
        
        group = groups[name]
        
        for layer in group:
            gslayer = self.catalog.get_layer(layer.name())
            if gslayer is None or overwriteLayers:
                self.publishLayer(layer, workspace, True)
                
        names = [layer.name() for layer in group]        
        
        layergroup = self.catalog.create_layergroup(destName, names, names)
        self.catalog.save(layergroup)
        
    def publishLayer (self, layer, workspace=None, overwrite=True, name=None):
        '''
        Publishes a QGIS layer. 
        It creates the corresponding store and the layer itself.
        If a pre-upload hook is set, its runs it and publishes the resulting layer  
        
        layer: the layer to publish, whether as a QgsMapLayer object or its name in the QGIS TOC.
            
        workspace: the workspace to publish to. USes the default workspace if not passed 
        or None 
        
        name: the name for the published layer. Uses the QGIS layer name if not passed 
        or None
        
        '''
        
        if isinstance(layer, basestring):
            layer = layers.resolveLayer(layer)   
                
        name = name if name is not None else layer.name()
        
        gslayer = self.catalog.get_layer(name)
        if gslayer is not None and not overwrite:
            return 
        
        title = name
        name = name.replace(" ", "_")        
          
        sld = self.publishStyle(layer, overwrite, name)
            
        layer = self.preprocess(layer)            
        self.upload(layer, workspace, overwrite, title)          

        if sld is not None:
            #assign style to created store  
            publishing = self.catalog.get_layer(name)        
            publishing.default_style = self.catalog.get_style(name)
            self.catalog.save(publishing)
            
    def preprocess(self, layer):    
        '''
        Preprocesses the layer with the corresponding preprocess hook and returns the path to the 
        resulting layer. If no preprocessing is performed, it returns the input layer itself
        '''    
        if not processingOk:
            return layer
        
        if layer.type() == layer.RasterLayer:                        
            try:
                hookFile = str(QSettings().value("/OpenGeo/Settings/GeoServer/PreuploadRasterHook", ""))
                alg = self.getAlgorithmFromHookFile(hookFile)                
                if (len(alg.parameters) == 1 and isinstance(alg.parameters[0], ParameterRaster) 
                    and len(alg.outputs) == 1 and isinstance(alg.outputs[0], OutputRaster)):
                    alg.parameters[0].setValue(layer)
                    if UnthreadedAlgorithmExecutor.runalg(alg, SilentProgress()):
                        return load(alg.outputs[0].value)
                    return layer
            except:
                return layer                                    
        elif layer.type() == layer.VectorLayer: 
            try:
                hookFile = str(QSettings().value("/OpenGeo/Settings/GeoServer/PreuploadVectorHook", ""))
                alg = self.getAlgorithmFromHookFile(hookFile)                
                if (len(alg.parameters) == 1 and isinstance(alg.parameters[0], ParameterVector) 
                    and len(alg.outputs) == 1 and isinstance(alg.outputs[0], OutputVector)):
                    alg.parameters[0].setValue(layer)
                    if UnthreadedAlgorithmExecutor.runalg(alg, SilentProgress()):
                        return load(alg.outputs[0].value)
                    return layer
            except:
                return layer
            
    def getAlgorithmFromHookFile(self, hookFile):
        if hookFile.endswith('py'):
            script = ScriptAlgorithm(hookFile)
            script.provider = Providers.providers['script']
            return script
        elif hookFile.endswith('model'):
            model = ModelerAlgorithm()
            model.openModel(hookFile)                
            model.provider = Providers.providers['model']
            return model
        else:
            raise Exception ("Wrong hook file")
        
    def addLayerToProject(self, name, destName = None):
        '''
        Adds a new layer to the current project based on a layer in a GeoServer catalog
        It will create a new layer with a WFS or WCS connection, pointing to the specified GeoServer
        layer. In the case of a vector layer, it will also fetch its associated style and set it
        as the current style for the created QGIS layer
        '''
        layer = self.catalog.get_layer(name)
        if layer is None:
            raise Exception ("A layer with the name '" + name + "' was not found in the catalog")
            
        resource = layer.resource        
        uri = uri_utils.layerUri(layer)  
               
        if resource.resource_type == "featureType":                             
            qgslayer = QgsVectorLayer(uri, destName or layer.title, "WFS") 
            if not qgslayer.isValid():
                raise Exception ("Layer at %s is not a valid layer" % uri)    
            ok = True
            try:
                sld = layer.default_style.sld_body  
                sld = adaptGsToQgs(sld)              
                sldfile = tempFilename("sld") 
                with open(sldfile, 'w') as f:
                    f.write(sld)             
                msg, ok = qgslayer.loadSldStyle(sldfile)                                                        
            except Exception, e:       
                ok = False
            QgsMapLayerRegistry.instance().addMapLayers([qgslayer])
            if not ok:
               raise Exception ("Layer was added, but style could not be set (maybe GeoServer layer is missing default style)")        
        elif resource.resource_type == "coverage":                        
            qgslayer = QgsRasterLayer(uri, destName or layer.title, "wcs" )
            if not qgslayer.isValid():
                raise Exception ("Layer at %s is not a valid layer" % uri)                  
            QgsMapLayerRegistry.instance().addMapLayers([qgslayer])

def createPGFeatureStore(catalog, name, workspace=None, overwrite=False,
    host="localhost", port = 5432 , database="db", schema="public", user="postgres", passwd=""):
    try:
        store = catalog.get_store(name, workspace)
    except FailedRequestError:
        store = None
    if store is not None:
        if overwrite:
            #if the existing store is the same we are trying to add, we do nothing
            params = store.connection_parameters
            if (str(params['port']) == str(port) and params['database'] == database and params['host'] == host
                    and params['user'] == user):
                return store
        else:
            msg = "There is already a store named " + name
            if workspace:
                msg += " in " + str(workspace)
            raise ConflictingDataError(msg)

    if store is None:
        store = catalog.create_datastore(name, workspace)
    store.connection_parameters.update(
        host=host, port=str(port), database=database, user=user, schema=schema,
        passwd=passwd, dbtype="postgis")
    catalog.save(store)
    return store
                        