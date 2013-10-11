.. _quickstart:

Quickstart tutorial
===================

This tutorial will guide you through some of the most basic tasks that can be performed using the OpenGeo Suite QGIS plugin.

Prerequisites
-------------

This tutorial assumes that QGIS and the OpenGeo Suite plugin has been already installed. It also assumes a local GeoServer instance and a PostGIS database installed with the parameters set by an OpenGeo Suite installation (GeoServer running on port 8080 and responding on ``http://localhost:8080/geoserver/`` and PostGIS running on port 54321). 

You may need to adapt the examples as needed to fit your specific installation.

Data
----

:download:`Download the example data <data/data.zip>` to be used in this tutorial. Extract this archive to a convenient directory.

Connecting to GeoServer
-----------------------

#. To start, open the OpenGeo Explorer by clicking the :guilabel:`OpenGeo` menu and selecting :guilabel:`OpenGeo Explorer`. The panel will appear on the right side of your QGIS window.

#. You will see that the :guilabel:`GeoServer catalogs` entry is empty. Click to select it and then click the :guilabel:`New catalog` button that will appear on the toolbar above the panel.

   .. note:: The buttons on the toolbar will change depending on the type of element selected in the tree.

#. The catalog creation dialog contains the default parameters for a local GeoServer instance.

   .. image:: img/quickstart/create_catalog.png

#. There is no need to modify the default values, so just click :guilabel:`OK`. The new catalog will appear in the :guilabel:`GeoServer catalogs` branch.

   .. image:: img/quickstart/catalog_entry.png

Publishing a QGIS project
-------------------------

#. In order to publish some data into that catalog, so the first thing to do is to create a workspace where we can put our data. Select the :guilabel:`Workspaces` entry and then click :guilabel:`New workspace` in the toolbar.

   .. todo:: Redo image, the URI doesn't work.

   .. image:: img/quickstart/create_workspace.png

#. Fill out the form in the dialog boxes with the inputs as shown above and click :guilabel:`OK`.

   .. todo:: List them here.

#. The new workspace should now appear in the list. It is not the default workspace, though, so to make it the default, select the workspace item, right-click and then select :guilabel:`Set as default workspace`. While not necessary, this will make the next few tasks a bit easier to perform.

   .. image:: img/quickstart/default_workspace.png

#. Open the QGIS project that is included in the example data (:file:`quickstart.qgs`). There should be five layers in your project in two groups.

   .. image:: img/quickstart/project.png

#. We will publish this project to GeoServer as it is, with those layers, groups, and the symbology associated with each layer.

   To publish the project as it is, just select the :guilabel:`QGIS project` entry in the explorer tree, and then click :guilabel:`Publish...`. You will see the following dialog:

   .. image:: img/quickstart/publish_project.png

#. Select the :guilabel:`quickstart` workspace as the destination workspace. Make sure the :guilabel:`Global group name` box is left blank. Click :guilabel:`OK` to start the publishing process.

#. Once finished, your catalog should look like this. 

   .. image:: img/quickstart/catalog_after_publish.png

   As you can see, a store has been created for each QGIS layer, and also the corresponding GeoServer layers and styles. Layers have been configured to use the corresponding styles.

Publishing a shapefile
----------------------

The sample data contains a shapefile named :file:`pt4.shp` that was not included in the QGIS project. We will add it to the already-published content.

#. There is no need to open the layer in QGIS. Just open the QGIS Browser, and locate the shapefile.

   .. image:: img/quickstart/file_in_browser.png

#. Select it and drag and drop onto the catalog item in the tree.

   .. image:: img/quickstart/drag_file.png

#. Since the ``quickstart`` workspace was set as the default, the layer will be added to that workspace. If you want to publish into another one, just drop it on the corresponding workspace item instead of the catalog one.

#. In this case, we want the layer to have the same style as the other layers we uploaded (which all share the same styling), so we can reuse one of the uploaded styles. To change the style, select the layer and then click the :guilabel:`Add style to layer` button. You will see the following dialog:

   .. image:: img/quickstart/add_style.png

#. Select the :guilabel:`pt1` style in the list. Make sure to check the :guilabel:`Add as default style` option as well.

   .. note:: You can also accomplish the same action by dragging the :guilabel:`pt1` style onto the layer item. That will not make it the default style, but you can then select it and click the :guilabel:`Set as default style` button.

#. Having switched the style for our ``pt4`` layer to use the one from ``pt1``, we can now remove the original ``pt4`` style. This can be done by right-clicking the style and selecting :guilabel:`Remove style from layer`. You can also delete it from the catalog itself (as it is not used by any other layer) by clicking the ``pt4`` element in the :guilabel:`Styles` branch and then selecting the :guilabel:`Delete` action.

Editing a style
---------------

One of the most interesting features of the Explorer is that you can use the QGIS interface to create your styles, without having to edit the SLD code manually. The sample project has already a style for each one of its layers, which was uploaded when we published the project to the GeoServer catalog. You can modify the style and then reimport it into the catalog, but you can directly edit any GeoServer style without actually having to have it open in QGIS as the style of a project layer.

To edit the style of the landuse layer (the one in the catalog that we have just uploaded, not the QGIS project one), locate the layer in the GeoServer tree, in the *Layers* branch. Under it, you should see the list of styles associated to the layer. Right click on it and select the :guilabel:`Edit...` option

..image:: img/quickstart/edit_style.png

This will open the QGIS symbology dialog, where you can make the changes you want to your style. When you close it, the style in your GeoServer catalog will be updated.



Publishing from PostGIS
-----------------------

There are other ways to publish our data. Instead of creating GeoServer layers that are based on shapefiles, we can import those shapefiles into a PostGIS database, and then create layers based on that database.

#. First create a database named ``quickstart``.

   .. note:: The details of this step are beyond the scope of this tutorial, as it must be done outside of QGIS using the ``psql`` command or the pgAdmin utility. 

#. Connect to the database using the OpenGeo Explorer by right-clicking the :guilabel:`PostGIS connections` item in the tree and selecting :guilabel:`New connection`.

   .. image:: img/quickstart/new_pg_connection.png

#. Set the parameters of the connection and click :guilabel:`OK`. The database should appear in the tree.

   .. image:: img/quickstart/connection.png

#. Now click the schema where you want to import your data, and select :guilabel:`Import files...`. The following dialog will appear:

   .. image:: img/quickstart/import_to_postgis.png

#. Click the button in the upper part of the dialog to select the files to import. Select the ``pt1.shp``, ``pt2.shp``, and ``pt3.shp`` files. Set the name of the destination table to :guilabel:`elevation`, and check the :guilabel:`Add to table (do not overwrite)` box. This will cause all files to be imported to a single table named ``elevation`` and not as three separate tables. The dialog should look like this.

   .. image:: img/quickstart/import_to_postgis2.png

#. Click :guilabel:`OK` and the data will be imported.

#. To create a GeoServer layer from that table, drag and drop the table onto the workspace item, just like when importing the shapefile.

#. The resulting GeoServer layer will have no style associated. You can solve that by dropping a style onto the layer.

Caching
-------

Once data is in our GeoServer catalog, we can use the OpenGeo Explorer panel to seed the tile cache of a particular layer.

#. In the :guilabel:`GeoWebCache` entry of the tree, you should have something like this:

   .. image:: img/quickstart/gwc.png

#. Click the layer that corresponds to the PostGIS-based layer (``elevation``) that was created in the previous section. Right-click and select :guilabel:`Seed...`. You will see a dialog to define the seeding to perform, where you should set the seeding parameters, for example as shown in the figure below:

   .. image:: img/quickstart/seed_dialog.png

#. Click :guilabel:`OK` and the seeding request will be sent. The description panel of the layer entry will change to reflect that a seeding operation has been launched.

   .. image:: img/quickstart/seed.png

#. The description is not updated automatically, but you can click the :guilabel:`Update` link to refresh it and see how it progresses, or the :guilabel:`Kill` link to abort the seeding operation.

Preprocessing data before publishing
-------------------------------------

The layers to upload require sometimes additional preprocessing, for instance if they are not the optimal format to provide the best performance once they are published. This preprocessing can be performed independently before publishing, but can also be included as part of the publishing operation itself. The OpenGeo explorer integrates with the QGIS processing framework and allows to define a process to be run on any layer before uploading it, publishing the resulting processed layer instead.

Processes are defined using the QGIS processing graphical modeler, and the process to use is specified in the Explorer configuration.

The example project contains a raster layer. If you published it as we have already seen, just dragging and dropping onto a workspace (we have only worked with vector layers so far, but raster layers are published in exactly the same way), the layer is published as is, with no modification. We can add a preprocessing hook that ensures that all uploaded raster layers have internal tiling and overviews/pyramids (both of which are not found in the example raster layer), which will result in a better performance when serving them from GeoServer.

#. Open the OpenGeo explorer configuration dialog using the corresponing menu entry in the OpenGeo menu.

   .. image:: img/quickstart/config.png

#. Find the :guilabel:`Raster preprocessing hook file` parameter. The data file that you downloaded contains an example model named ``raster_hook.model`` that adds tiling and pyramids to a raster layer. Locate it and enter the path to it as value of the parameter. This will cause the model to be run before the data is uploaded, and the resulting output to be imported instead of the original layer.

#. Upload the example raster layer. The preprocessing hook will be run before the upload. To disable it for future uploads, just go to the configuration and change the value of the corresponding value to an empty string, so it doesn't point to any valid model file.

The sample data zip file contains another example hook that can be used for vector layers. This time, it is not a model file, but a python script (the Explorer support both ways of definign a Processing algorithm), and it will export the selected features to a new layer, so only those features will be later uploaded. If the layer you are uploading is not open in QGIS (such as when you export dragging it directly from the QGIS browser), the hook will have no effect at all (since it is not open, a selection does not exist). If, however, the layer is loaded and a selection exists, only the selected features will be uploaded. If no features are selected, the whole layer will be uploaded. The corresponding script file is named ``vector_hook.py`` and to use it you should enter the path to it in the :guilabel:`Vector preprocessing hook file` parameter in the config dialog.








