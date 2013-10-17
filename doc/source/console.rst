Configuring a GeoServer catalog from the console
=================================================

A GeoServer catalog can be configured from the QGIS Python console.

Open the QGIS console and import the ``opengeo`` package

::

	import opengeo

Now create a GeoServer catalog

::

	catalog = opengeo.createGeoServerCatalog()

Since we have passed no arguments to the method, it will use the default ones, which correspond to a GeoServer available at localhost and with the default user (``admin``) and password(``geoserver``).

Now, ``catalog`` contains and object that has a set of convenience methods to communicate between QGIS and GeoServer. This will allow you to do all the configuration in QGIS (setting the name of a layer, defining its symbology, creating layer groups, etc), and then publish the content of your project easily. The functionality that you can access through the classes and methods that this plugin adds is designed to make a direct correspondence between the current QGIS project you are working on and the content of your GeoServer catalog. This actually turns your QGIS into a frontend of GeoServer, allowing you to easily configure it.

Let's see some examples. First, let's create a new store and a layer based on it.

:download:`Download the example data <data/data.zip>`. It contains a QGIS project with some data that we will use for the examples in this short tutorial. Open the project.

We are going to publish the ``pts1`` layer. Its name in the QGIS project is the name that it will have when published. You can change it if you want, but do not forget to also change the corresponing references to it in the examples that follow.

Double click on its name to get to the properties dialog, and create a symbology for the layer if you want to have a different rendering than the default one.

Now, run the following on the QGIS console.

::

	catalog.publish("pts1")

We are passing the name of the layer in the QGIS project to identify it. The method also accept a QgsMapLayer object.

This will cause the store to be created and a style of the same name to be published. A layer that uses that store and style will be created as well. You can pass a string to the ``name`` parameter, to use a different name for the published layer.

When publishing a layer this way, you do not have to worry about the layer origin. The plugin code will take care of converting your data to a suitable format to be uploaded to GeoServer. If the format is not supported by GeoServer, an intermediate Shapefile will be created, and then used to create the corresponding datastore from which the layer will then be published.

If you try to publish a QGIS layer that is based on a PostGIS connection, a PostGIS datastore will be created, instead of a file--based one. That gives you an easy way of creating a PostGIS--based layer in GeoServer, since you just have to create the corresponding connection in QGIS, create a QGIS layer from one of its tables, and then pulish it with the above code. The corresponding store and feature type will be added to GeoServer, and your layer, including the style that you set for it in QGIS, will be published.

.. note:: For now, all operation have an aggresive overwrite behaviour by default, so if a resource with the specified name exists in the GeoServer catalog, it will be overwritten and replaced.

You can also create layer groups in GeoServer, by creating the equivalent groups in QGIS and then telling it to upload those same groups.

The example project contains a group named *geology_landuse*. To create the corresponding layer group in your GeoServer catalog, just enter the following in the console.

::

	catalog.publishGroup("geology_landuse")

If the layers in the group do not exist in the GeoServer catalog, they will be created automatically, creating the corresponding stores and styles as we have seen. If they already exist, they will be used and not updated. You can overwrite the existing layers by setting the ``overwrite`` parameter to *True*.

::

	catalog.publishGroup("geology_landuse", overwrite = True)


Apart from moving layers and element from the current QGIS project to a GeoServer catalog, we can also move them the other way, easily adding remote layers to a QGIS project.

To add a layer named "mylayer" to the current project, enter this in the console.

::

	catalog.addLayerToProject("mylayer")

That will create a layer in the current QGIS project which is connected to the GeoServer layer, and, in the case of it being a vector layer, it will download its associated style and use it to set the symbology of the created QGIS layer. Since raster layers do not support SLD styles in QGIS, they will not get styled.

If the layer that is created in the QGIS project is a vector layer, it will be connected to the corresponding store in GeoServer using the WFS endpoint. If is is a raster layer, it will create a WCS layer. In all cases, no data is downloaded, but a connection is created instead.

Additional functionality is available in the OGCatalog class. Check it's documentation to know more about its usage.
