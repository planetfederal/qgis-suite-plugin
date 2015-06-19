.. _usage:

Usage
=====

OpenGeo Explorer is launched from the :guilabel:`OpenGeo` menu:

.. todo:: Link to menu image

The brings up a panel in QGIS. The main element of this panel is the tree. It has the following main branches, each of which deals with a different component.

* GeoServer Catalogs
* PostGIS Connections
* QGIS Project

.. note:: A **GeoWebCache** branch is found under **Geoserver Catalogs**, since GeoWebCache is integrated into GeoServer.

The **GeoServer Catalogs** branch contains a list of the catalogs of all connected GeoServer instances. Once instances are added to this branch, you can interact with this GeoServer form within this panel, including publishing layers and styles.

The **PostGIS Databases** branch contains a list of all connected PostGIS databases. Its functionality resembles that of the DB Manager in QGIS. Once databases are added here, you can interact with them from within this panel, including viewing and adding tables.

The **QGIS Project** branch contains the elements of the current QGIS project.

.. note:: The elements in the QGIS Project branch are presented with a structure that more resembles the elements in GeoServer, making publishing easier.

The lower part of the panel contains an information window showing the description of the currently selected item, and also contains links to actions that are related to the current element. 

.. figure:: img/description_panel.png

.. note:: When the panel is undocked, the information window appears to the right of the tree.

   .. figure:: img/undocked.png

The information window can also show tables where parameters can be edited. The one shown below corresponds to the :guilabel:`Settings` element of a GeoServer catalog.

.. figure:: img/description_table.png

Accessing the functionality of OpenGeo Explorer is done through context menus (right-clicking), or through the buttons in the toolbar above the tree. These buttons change depending on what is selected, and are identical to the items found in the context menu.

To see command functionality used in OpenGeo Explorer, please see the :ref:`tutorial` page. For a comprehensive reference of all possible options, please see the :ref:`actions` section.

Multiple selection
------------------

You can select multiple elements of the same type (i.e. multiple QGIS layers), to automate operations. For instance, let's say that you have several layers in your current project. Select them all (click while pressing the Ctrl or Shift keys) and then right--click and select :guilabel:`Publish...`. You will get see to a dialog like the following one.

.. figure:: img/publish_layers_multiple_catalogs.png


This is the same dialog that appears in case of publishing a group to a GeoServer catalog. Notice, however, that in the case of a group, all layers for that group have to be imported into the catalog where the group will be created, so the layer publishing dialog doesn't let you select the catalog, but only the workspace for each layer. In this case, there is more flexibility, so an additional column is show, which can be used to select the catalog for each layer. Changing the selected catalog at a given row will automatically update the list of workspaces in that row, so it contains the workspaces of that catalog.

If only one catalog exists in the Explorer tree, the catalog column will not be shown.

Configure the catalog (if available) and workspace you want to upload each layer to, and a multiple upload will be executed.

Another task than can be done with a multiple selection is creating a new group. Just select a set of layers, right--click on them and select :guilabel:`Create group...`. A new group will be created with those layers, using the default style of each of them. For a more fine-grained definition of the group, remember that you can use the :guilabel:`Create new group...` option in the :guilabel:`GeoServer Groups` item

Double-clickingtree items
-------------------------

Certain items respond to double-clicking. If the corresponding element can be edited, the edition can be started by double-clicking on it instead of using the corresponding context menu entry. For instance, double-clicking on a GeoServer group item will open the dialog to define the layers that are included in that group.

Drag and drop operations
------------------------

The Explorer tree supports drag & drop, and you can use it to relocate elements, publish data or edit the configuration of an element. 

.. figure:: img/dragdrop.png


Below you can find more information about the operations that can be performed this way.

- Dragging a QGIS layer item onto a GeoServer item element. It will publish the layer on the workspace where the item was dropped, or on the parent workspace if the destination element is of type Resource/Store. Otherwise, it will publish to the default workspace.
- Dragging a GeoServer layer item onto a GeoServer group element. It adds the layer to the group, using its default style.
- Dragging a GeoServer or QGIS style item onto a GeoServer layer. It adds the style to the list of alternative styles of the layer.
- Dragging a QGIS style into the :guilabel:`Styles` element of a catalog or a catalog item itself. It adds the style to that catalog.
- Dragging a QGIS style into a GeoServer layer element. It publishes the style to the catalog the layer belongs to, and then adds the style to the list of alternative styles of the layer.
- Dragging a QGIS group element into the :guilabel:`Groups`, :guilabel:`Workspaces`, :guilabel:`Layers` of a catalog, or the catalog item itself. The group is published and all layers that do not exist in the catalog and need to be published as well, their corresponding stores will be added to the default workspace. If dropped on a workspace item, that workspace will be used as destination.
- Dragging a GeoServer layer item onto the :guilabel:`GeoWebCache layers` item of the same catalog. It will add the corresponding cached layer for the dragged layer.
- Dragging a QGIS layer into a PostGIS connection or schema item. It will import the layer into the corresponding PostGIS database. The import dialog is shown before importing.
- Dragging a QGIS layer into a PostGIS table item. It will append the dragged layer to the existing table, not overwriting it. No checking is performed, so the schema of the imported layer should match the schema of the table. Otherwise, PostGIS will throw an error.
- Draggin a PostGIS table item into a GeoServer catalog or workspace item. It will publish a new layer based on that table, using the item workspace or the default workspace in case of dropping onto a catalog item


Multiple elements can be selected and dragged, as long as they are of the same type.

You can also drag elements from outside of the OpenGeo Explorer itself. For instance, you can open the QGIS browser, select some files with raster or vector data and drag and drop them into a PostGIS database or Geoserver catalog element in the explorer. That will cause the data in those files to be imported into the corresponding database or catalog. Format conversion will be performed automatically if needed.

.. figure:: img/dragdrop_external.png


If the dragged files are not opened in the current QGIS project, no style will be uploaded along with them when publishing to a GeoServer catalog.

In general, any operation that can be performed dragging a QGIS layer item within the Explorer tree can also be performed dragging an element in the QGIS browser that represents a layer.

Also, elements from the explorer can be dropped onto the QGIS canvas. GeoServer layers can be dropped onto the QGIS canvas to add them to the project. The corresponding WFS/WCS layer will be created as in the case of using the :guilabel:`Add to QGIS project` menu option, already described. Notice that, however, the style of the layer will not be used in this case, and the layer that will be added to the QGIS project will have a default style assigned to it.

Dragging and dropping a PostGIS table will cause a new layer to be added to the QGIS project, based on that table.


Preprocessing data
------------------

The layers to upload sometimes require preprocessing, for instance if they are not in the optimal format to provide the best performance once they are published. This preprocessing can be performed independently before publishing, but can also be included as part of the publishing operation itself.

The OpenGeo Explorer integrates with the QGIS Processing Framework and allows you to define a process to be run on any layer before uploading it, publishing the resulting *processed* layer instead.

Processes are defined using the QGIS processing graphical modeler or as python scripts, and the process to use is specified in the Explorer configuration.

The sample data zip file contains an example hook that can be used for vector layers. It will export the selected features to a new layer, so only those features will be later uploaded. If the layer you are uploading is not open in QGIS (such as when you export dragging it directly from the QGIS browser), the hook will have no effect at all (since it is not open, a selection does not exist). If, however, the layer is loaded and a selection exists, only the selected features will be uploaded. If no features are selected, the whole layer will be uploaded. 

Follow these steps to enable the upload hook

#. Open the OpenGeo Explorer configuration dialog from the OpenGeo menu.

   .. figure:: ../config/img/config.png

      OpenGeo Explorer settings

#. Find the :guilabel:`Vector preprocessing hook file` parameter. The data file that you downloaded contains an example model named ``vector_hook.py``. Locate it and enter the path to it as value of the parameter. This will cause the model to be run before the data is uploaded, and the resulting output to be imported instead of the original layer.

#. Make a selection in one of the project layers and upload it to GeoServer. The preprocessing hook will be run before the upload and only the selected features will be uploaded. To disable it for future uploads, just go to the configuration and change the value of the corresponding value to an empty string, so it doesn't point to any valid model or script file.

