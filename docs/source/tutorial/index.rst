.. _tutorial:

Tutorial
========

This tutorial will guide you through some of the most common tasks that can be performed using OpenGeo Explorer.

Prerequisites and data
----------------------

This tutorial assumes that QGIS with OpenGeo Explorer has been already :ref:`installed <install>`. It also assumes a local GeoServer instance and a PostGIS database installed with the parameters set by a standard OpenGeo Suite installation:

* GeoServer running on port 8080 and responding on ``http://localhost:8080/geoserver/``
* PostGIS running on port 5432

You may need to adapt the examples as needed to fit your specific installation.

Next, :download:`Download the example data <../data/quickstart_data.zip>` to be used in this tutorial. Extract this archive to a convenient directory.

Connecting to GeoServer
-----------------------

#. To start, launch OpenGeo Explorer by clicking the :guilabel:`OpenGeo` menu and selecting :guilabel:`OpenGeo Explorer`. The panel will appear on the right side of your QGIS window.

   .. figure:: img/explorer.png

      OpenGeo Explorer

#. You will see that the :guilabel:`GeoServer Catalogs` entry is empty. Click to select it and then click the :guilabel:`New catalog` button.

   .. note:: The buttons on the toolbar will change depending on the type of element selected in the tree.

   .. note:: You can also right-click on elements in OpenGeo Explorer.

#. The catalog creation dialog contains the default parameters for a local GeoServer instance.

   .. figure:: img/create_catalog.png

      Default parameters

#. There is no need to modify the default values, so just click :guilabel:`OK`. The new catalog will appear in the :guilabel:`GeoServer catalogs` branch.

   .. figure:: img/catalog_entry.png

      Creating a connection to a GeoServer catalog

   .. note:: If you see an error saying "Could not connect to catalog", make sure that GeoServer is running and on the port specified.

Publishing a QGIS project
-------------------------

In order to publish data into the GeoServer connected to in the previous step, we will first create a workspace where we can put our data.

#. Expand the :guilabel:`Default GeoServer catalog` tree.

#. Click the :guilabel:`GeoServer Workspaces` entry to select it and then click the :guilabel:`New workspace` button.

#. Fill out the form in the dialog boxes with the inputs as shown above and click :guilabel:`OK`.

   * **Name**: ``quickstart``
   * **URI**: ``http://quickstart``

   .. figure:: img/create_workspace.png

      Creating a new workspace in GeoServer

#. Expand the :guilabel:`GeoServer Workspaces` entry, and the new workspace should now appear in the list.

#. To make this new workspace the default, select the workspace item, and click the :guilabel:`Set as default workspace` button.

   .. figure:: img/default_workspace.png

      Default workspace

#. Open the QGIS project that is included in the example data (:file:`quickstart.qgs`). There should be five layers in your project in two groups.

#. This is what the project will look like:

   .. figure:: img/project.png

      Quickstart sample project

   It contains the following layers:

   * 

#. We will publish this project to GeoServer as it is, with those layers, groups, and the symbology associated with each layer.

   To publish the project as it is, just select the :guilabel:`QGIS project` entry in the OpenGeo Explorer tree, and then click the :guilabel:`Publish...` button. You will see the following dialog:

   .. figure:: img/publish_project.png

      Publish project dialog

#. Select the :guilabel:`quickstart` workspace as the destination workspace. Make sure the :guilabel:`Global group name` box is left blank. Click :guilabel:`OK` to start the publishing process.

#. For each top-level layer, a dialog will display, giving you an opportunity to rename the layers and layer groups when published to GeoServer. You don't need to rename anything, so click :guilabel:`OK` in each of the three dialogs.

   .. figure:: img/publish_dem.png

   .. figure:: img/publish_geology_landuse.png

   .. figure:: img/publish_elevation.png

#. Once finished, your catalog should look like this:

   .. figure:: img/catalog_after_publish.png

      GeoServer catalog after published project

   A store has been created for each QGIS layer, and also the corresponding GeoServer layers and styles, all in the ``quickstart`` workspace. Layers have also been configured to use the corresponding styles.

You can now verify these layers and groups in your GeoServer instance.

Publishing a shapefile
----------------------

The sample data contains a shapefile named :file:`pt4.shp` that was not included in the QGIS project. We will add it to the already-published content. It is not necessary to open/view the layer in QGIS to publish it to GeoServer.

#. Open the QGIS Browser (:menuselection:`View --> Panels --> Browser` if it is not already open) and locate the shapefile.

   .. figure:: img/file_in_browser.png

      File in the QGIS Browser

#. Click to select the file and drag it onto the :guilabel:`GeoServer Workspaces` catalog item in the OpenGeo Explorer tree.

#. A dialog will display, asking you to name the layer. Click :guilabel:`OK`.

   .. figure:: img/upload_rename.png

      Shapefile upload dialog

   .. note:: As the ``quickstart`` workspace was set as the default, the layer will be added to that workspace. If you want to publish into another workspace, drag and drop the file on to the corresponding workspace entry.

#. The shapefile is now published in GeoServer, but is not currently added to the QGIS project, so it won't be displayed in the map window.

#. In this case, we want the layer to have the same style as the other layers we uploaded (which themselves all share the same styling), so we can reuse one of the uploaded styles. To change the style, expand the tree and select the :guilabel:`pt4` layer in the :guilabel:`GeoServer Layers` list (*not* :guilabel:`GeoServer Workspaces`). Then click the :guilabel:`Add style to layer` button.

#. Select the :guilabel:`pt1` style in the list. Make sure to check the :guilabel:`Add as default style` option as well.

   .. figure:: img/add_style.png

      Add style to layer dialog

   .. note:: You can also accomplish the same action by dragging the :guilabel:`pt1` style onto the layer item. That will not make it the default style, but you can then select it and click the :guilabel:`Set as default style` button.

#. Click :guilabel:`OK`.

#. While it's not necessary, we can now remove the original style. This can be done by right-clicking the ``pt4`` style inside the ``pt4`` layer and selecting :guilabel:`Remove style from layer`. You can also delete it from the catalog itself (as it is not used by any other layer) by clicking the ``pt4`` element in the :guilabel:`GeoServer Styles` branch and then clicking the :guilabel:`Delete` button.

   .. figure:: img/new_default_style.png

Editing a style
---------------

One of the most interesting features of the OpenGeo Explorer plugin is that you can use QGIS to create your styles, and then publish them directly to GeoServer. This means that you have access to all of graphical editing capabilities in QGIS, without the need to edit SLD code.

While the project already has a style for each of its layers, you can also directly edit any GeoServer style without it being part of a QGIS project. We will show that below, by editing the style of the ``landuse`` layer in GeoServer.

#. In the OpenGeo Explorer tree, locate the ``landuse`` layer in :guilabel:`GeoServer Layers`. Under it, you should see the list of styles associated with the layer, which in this case will only be the ``landuse`` style.

   .. figure:: img/edit_style.png

      Style associated with the layer

#. Select the style and click the :guilabel:`Edit` button. This will open the QGIS symbology dialog, where you can make the changes you want to your style. When you close it, the style in your GeoServer catalog will be updated.

   .. note:: There is also an :guilabel:`Edit SLD` option, but that is a different task.

   .. figure:: img/layer_properties_style_edit.png

      QGIS style editor

#. Let's make some small edits to this style. In the QGIS style dialog, double click the :guilabel:`agricultural_areas` row.

#. In the :guilabel:`Style properties` dialog, click the :guilabel:`Color` button and change the color.

   .. figure:: img/rule_properties.png

      Style rule with a changed color (purple)

#. Click :guilabel:`OK`.

#. Delete the bottom rule that contains :guilabel:`(no filter)`. Click to select it and click the :guilabel:`Remove rule` button (the red minus).

#. Click :guilabel:`OK`.

The style has been changed in GeoServer. This can be verified in OpenGeo Explorer by selecting the same style and clicking the :guilabel:`Edit SLD` button and viewing the style code. It can also be viewed in GeoServer's Layer Preview.

.. note:: The style change will not be reflected in the QGIS viewing window, because it is reading from the local project and not from GeoServer.

.. figure:: img/landuse_before.png

   Original landuse style

.. figure:: img/landuse_after.png

   Changed landuse style

Publishing from PostGIS
-----------------------

You can also create layers in GeoServer based on database tables, all through OpenGeo Explorer.

We will see this by first importing those shapefiles into a PostGIS database, and then creating layers.

#. First create a database named ``quickstart``. Make sure this database is spatially enabled.

   .. note:: The details of this step are beyond the scope of this tutorial, as it must be done outside of QGIS using PostgreSQL command-line utilities like ``psql`` or the ``pgAdmin`` utility. An example using the command line would look like this:

      .. code-block:: console

         createdb -U postgres quickstart
         psql -U postgres -d quickstart -c "create extension postgis;"

#. Connect to the database using the OpenGeo Explorer by selecting :guilabel:`PostGIS connections` and then clicking the :guilabel:`New connection` button.

#. Leave all fields in the form as defaults. Add ``quickstart`` in the :guilabel:`Database` field.

   .. figure:: img/new_pg_connection.png

#. Set the parameters of the connection and click :guilabel:`OK`. The database should appear in the tree.

   .. figure:: img/pg_connection.png

#. Expand the tree and select the schema where you want to import your data (usually called ``public``).

#. Click the :guilabel:`Import files` button.

#. In the resulting dialog, click the button in the upper part of the dialog to select the files to import. Select the ``pt1.shp``, ``pt2.shp``, and ``pt3.shp`` files. Set the name of the Table to :guilabel:`elevation`, and check the :guilabel:`Add to table (do not overwrite)` box. This will cause all files to be imported to a *single* table named ``elevation`` and not as three separate tables. 

   .. figure:: img/import_to_postgis.png

#. Click :guilabel:`OK`.

The data will be imported. To create a GeoServer layer from that table, drag and drop the :guilabel:`elevation` entry onto :guilabel:`GeoServer Workspaces`, just like when importing the shapefile above.

.. figure:: img/pg_elevation.png

   Viewing the combined ``elevation`` table in QGIS.

Publishing a TIF file
---------------------

Raster layers are published in a similar way to vector layers. The example data includes a raster layer named :file:`dem.tif`` that can be uploaded to GeoServer in the two ways we've seen before:

* Drag file name from the QGIS Browser to :guilabel:`GeoServer Workspaces`.

* Add to the current project, then select the layer in the :guilabel:`QGIS Layers` list in OpenGeo Explorer and click :guilabel:`Publish`.

In either case, a new raster store will be created in the catalog, and the corresponding layer will be published.

.. note::

   This file was already part of the project that was uploaded, so if publishing again, you will need to rename the layer, or the existing layer will be overwritten.

   .. figure:: img/publish_tif_overwrite.png

      Overwriting a layer during publish

When publishing directly from the file, a default style will be used. Single-band layers will use a black-to-white color ramp, and all other layers are assumed to be 3-band RGB color images.

Caching
-------

Once data is in the GeoServer catalog, we can use OpenGeo Explorer to seed the tile cache of a particular layer.

#. In the :guilabel:`GeoWebCache Layers` entry, you will see a list of every cached layer in GeoServer:

   .. figure:: img/gwc.png

      Cached layers

#. Select the ``elevation_table`` layer (from PostGIS) and click the :guilabel:`Seed` button. You will see a dialog to define the seeding task to perform, along with all parameters, as shown in the figure below:

   .. figure:: img/seed_dialog.png

      Seed dialog

#. Click :guilabel:`OK` to start the seeding process. The description panel of the layer entry will change to reflect that a seeding operation has been launched.

   .. figure:: img/seed.png

#. The description is not updated automatically, but you can click the :guilabel:`Update` link to refresh the view or the :guilabel:`Kill` link to abort the seeding operation.
