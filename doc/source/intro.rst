Introduction
============

This section will give a basic introduction to the functionality of the OpenGeo Suite plugin for QGIS.

Installing the current development version
------------------------------------------

The plugin repository is updated frequently. However, it is not guaranteed that it will contain the same code that can be found in the GitHub repository. If you want to be sure that you are using the latest development version, follow the steps described in the :ref:`developers` section.

Installing from a zip file
--------------------------

If you have a copy of the plugin code in a zip file, you can install it unzipping it into the QGIS plugins folder. In Windows, it should be something like ``C:\Users\<your_user>\.qgis2\python\plugins``. In Linux/Mac, it should be in ``~/.qgis2/python/plugins``. Copy the ``opengeo`` folder in your zip file into your plugins folder. You should end up having a ``.qgis2\python\plugins\opengeo`` folder with the code of the plugin and the required subfolders. The ``plugin.py`` file should be on that folder.

Version support and limitations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This plugin is targeted at the elements of OpenGeo Suite, and it is tested with the versions of those element included in the latest release of the Suite (4.0). However, you can use most of the functionality if you are using individual installations of elements such as GeoServer and PostGIS.

The current version of the plugin is targeted at GeoServer 2.3.x. If you are using an older version, you might encounter some problems, and some elements might not be correctly configured due to differences in the way they are handled by GeoServer or in changes in the REST API that the plugin uses to communicate with GeoServer. Although most things should work fine if connecting to a GeoServer 2.2.x catalog, the following are some of the incompatibilities that have been detected.

* Empty groups. Layers belonging to a group are not found, since the group definition has a different structure
* Styles belonging to a given namespace are not found. Only styles with no namespace are reported if using GeoServer 2.2.x

To check the version of your catalog, just select the catalog in the tree and look at the description tab. 

.. figure:: img/intro/about.png
  :align: center

If you do not see information like that, it is likely that your catalog uses a GeoServer version that doesn't support that operation. In this case, it will not support the other operations that cause problems, so you will probably find some issues when working with the catalog through the plugin.

When connecting to a catalog, the explorer tries to check the version. If it cannot detect the version or it cannot confirm it is the target version, it will ask you before adding the catalog.

.. figure:: img/intro/version_warning.png
  :align: center


Even if you are using the correct version of GeoServer, some limitations still exists. Below is a list of know limitations and issues than might appear.

* CRS. GeoServer might encounter problems when a custom CRS is used in QGIS. The CRS definition that works correctly when rendering the layer in QGIS might not work when importing the layer into GeoServer. Usually this results in a layer that is published but doesn't have a CRS set and is not enabled. You can correct that manually, selecting the layer in the Explorer tree and modifying its CRS.

  Notice that layers are imported using the SRS defined in the original data source (i.e., the ``prj`` file if using a shapefile). Setting a different CRS using the :guilabel:`Set Layer CRS` option in the QGIS TOC will not have any effect when importing the layer into GeoServer, unless you save the layer with that CRS and the CRS definition is stored along with the layer data.

* Layer names. The OpenGeo Explorer uses the GeoServer REST API to get the list of layers in a catalog. The REST API describes layers without workspace, that meaning that if you have two layers with the same name and in different workspaces (for instance, ``ws1:mylayer`` and ``ws2:mylayer``), they will be shown as just one (``mylayer`` in this case).

  When this happens, the situation is ambiguous and OpenGeo Explorer cannot differentiate between layers with the same name but belonging to different workspaces. The layer, as describe by the REST API, is added to the Explorer tree, but it only represents one of the several layers that share the same name. To indicate this, the layer is shown with a warning icon, and a warning message is displayed in the layer description.

  .. figure:: img/intro/duplicated_layer.png
     :align: center


Another important limitation is due to the different versions of the SLD standard that QGIS and GeoServer support. Read the :ref:`styling_limitations` section to know more about it.


Usage
-----

The OpenGeo Suite explorer is launched from the :guilabel:`OpenGeo` menu and it looks like this.

.. figure:: img/intro/explorer.png
  :align: center

The main element of the explorer is the explorer tree. It has the following main branches, each of which deals with a different component.

* GeoServer catalogs
* PostGIS connections
* QGIS project

A :guilabel:`GeoWebCache` branch is found under the :guilabel:`Geoserver catalogs` branch, since GeoWebCache is integrated into GeoServer.

The :guilabel:`GeoServer catalogs` branch contains the catalogs that you are connected to, and with which you can interact from the explorer. It is empty when you start the explorer, and you can add as many connections as you want to it.

The :guilabel:`QGIS Project` branch contains the elements of the current QGIS project. These elements, however, are presented with a structure that differs from the QGIS TOC, and resembles the structure of elements in GeoServer. This way, it is easy to understand the relation between both the QGIS project and the GeoServer Catalogs.

The :guilabel:`PostGIS databases` branch contains a list of all available PostGIS connections in QGIS. Its functionality resembles that of the QGIS built--in DB Manager.

In the lower part to will see a panel which shows the description of the currently selected item. When the explorer window is docked, the description panel is found on its lower the lower part. If you undock the window, it will be placed on the right--hand side of it, to make better use of the available space. The image below shows the undocked configuration.

.. figure:: img/intro/undocked.png
  :align: center

The description panel shows information about the currently selected element, but also contains links to actions that affect or are related to the current element. As an example, below you can see the description panel corresponding to a GeoServer layer element.

.. figure:: img/intro/description_panel.png
  :align: center

Use the hyperlinks to perform the corresponding actions based on the current element.

The description panel can also show tables where parameters can be edited. The one shown below corresponds to the :guilabel:`Settings` element of a GeoServer catalog.

.. figure:: img/intro/description_table.png
  :align: center


Most of the functionality of the explorer is accessed through context menus, right--clicking on the elements that you will find in the branches described above. Also, when you select an element in the tree, buttons in the toolbar in the upper part of the explorer window are updated to show the available actions for that element. These actions correspond to the ones shown in the context menu when you right--click on the element, so you have different ways of accesing the same funcionality. As it was explained before, the *Description* panel is also interactive.

To start working with the explorer and know more about how to use it, check the :ref:`quickstart` page. For a more complete reference, a detailed description of all the available actions for each kind of element in the Explorer tree is available at the :ref:`actions` section.

GeoServer and PostGIS synchronization
-------------------------------------

Except for the :guilabel:`QGIS Project` item, all remaining items (PostGIS and GeoServer ones) are not automatically updated when the element they represent changes. A change in a PostGIS database performed outside of the plugin, or a change in the catalog performed using, for instance, the GeoServer Web interface, they will not trigger an update in the OpenGeo Explorer tree. 

All items have a :guilabel:`Refresh` option. Use it to update the content of a given entry in the tree and keep it synchronized with the corresponding catalog or database.

Reporting errors
----------------

When an error is found, a message is shown in the QGIS message bar.

.. figure:: img/intro/error-bar.png
  :align: center

This error might be caused by a wrong usage (for instance, if you are trying to connect to a catalog that does not exist), or by a bug in the plugin. To help us fix this second case, you can report the error by clicking on the :guilabel:`Report error` button that appears in the message bar. This will cause the full error stack trace to be sent automatically, so we can check it and find out the cause of the error. No personal information is sent along with it.

To check the stack trace yourself, click on the :guilabel:`View more` button.

If no button is pushed, the message bar will remain visible for 15 seconds. You can close it using the close icon on its right--hand side.


.. _configuration:

Configuration
-------------

Along with the menu entry that starts the Explorer, you will find an entry that opens the configuration window, which looks as shown next.

.. figure:: img/intro/config.png
  :align: center

Use the parameters in this dialog to configure the Explorer to your particular needs. The properties that can be configured are described in detail below.

Tabbed vs single-tab interface
------------------------------

By default, the Explorer shows all categories (GeoServer, PostGIS) in a single panel, as branches in a tree. If you enable the multi-tab user interface, each category is put in a separate tab, and each tab contains a panel with a tree of elements belonging to the corresponding category, as shown in the next figure.

.. figure:: img/intro/multi-tab.png
  :align: center


Functionality can be accessed in the same way as in the default interface, by right clicking on an element or selecting it and using the buttons that will appear in the toolbar on the upper part of the panel. Drag & drop functionality is limited to elements within the same category. 

In case they exist, subcategories (such as layers, workspaces, etc., in the case of a GeoServer catalog) can be switched using the buttons on the lower part of the panel.

When you change the type of UI by changing the corresponding value in the configuration dialog, the Explorer interface is not automatically changed. Restarting QGIS is needed for the change to take effect.

.. _gs_connections:

Keeping a list of previous GeoServer connections
------------------------------------------------

If you enable this option, whenever you connect to a catalog, the information that defines that connections is kept between sessions. Next time that you start QGIS and the OpenGeo Explorer, you will see the catalogs item populated with all the previous connections, as shown in the next picture.

.. figure:: img/intro/gray_catalog.png
  :align: center

Retrieving information from each connection might take a long time and cause QGIS to take too long to start up. For this reason, catalog data is fetch on request and not automatically when starting the OpenGeo Explorer. You should refresh the catalog item to populate it. Unpopulated catalogs are shown with a gray icon.

All information needed to connect to the catalog is kept, except sensible values such as the password or the private key path if using certificates. They have to be entered when the catalog is refreshed.

To delete a catalog from the list of previous connections, use the :guilabel:`Remove` option of the catalog item in the Explorer tree.

Using the GeoServer importer API
--------------------------------

.. note: The importer API is currently disabled in the OpenGeo Explorer, and changing the value of the parameter will have no effect at all. All uploads are done using the REST API.

By default, layers are uploaded to a GeoServer catalog using the GeoServer REST API. As an alternative, the importer API can be used to provide a better and more responsive upload, specially in the case of large uploads with multiple layers or when large layers are being uploaded.

OpenGeo Suite 4.0 includes the importer API by default, but an independent GeoServer instance normally does not contain it, even if it is a recent version that is supported by the Explorer plugin. Make sure that you are running OpenGeo Suite or that you have manually installed the importer API on your GeoServer before setting this configuration parameter. 

Pre-upload Processing hooks
---------------------------

If you need to preprocess you data before it is uploaded, you can set up a pre-upload hook that will be run on any layer before it is sent to GeoServer. Instead of the original layer, the result of that hook will be uploaded.

Pre-upload hooks are defined separately for raster and vector layers. In both cases, they are defined as the path to a Processing model (.model) or script (.py) file. That algorithm defined by that hook file will be loaded and executed to obtain the final layer to upload. Creation of Processing models and scripts is not covered in this text. Please refer to the `Processing chapter in the QGIS manual <http://qgis.org/es/docs/user_manual/processing/index.html>`_  to know more about it.

In the case of raster layers, the hook algorithm must have a single input of type raster layer and a single output, also of type raster layer. In the case of vector layers, both input and output must be of type vector layer. If the selected model does not exist or does not have the required characteristics, it will just be ignored, and the original layer will be uploaded without any preprocessing.

For these functionality to be available, you need a version of Processing more equal or higher that 2.0.1.1. If you just install QGIS 2.0.1, you will have 2.0.1.1 installed (Procesing versions are named after the QGIS version, with an extra number, to indicate the number of independent releases of the plugin after the corresponding QGIS version has been released), so you have to update it using the QGIS Plugin Manager. If your QGIS installation doesn't have a valid Processing version, you can still use the remaining funcitonality of the OpenGeo Explorer, but pre-upload hooks will not be run, and the correspoding parameters in the config dialog will not be shown. After updating you Processing plugin, a restart is needed so the OpenGeo Explorer can update itself to the new configuration.

Other parameters
----------------

* *Delete style when deleting layer*. If a GeoServer layer is deleted and is the only layer using a given style, the style will be also deleted if this parameters is checked

* *Delete resource when deleting layer*. If this parameter is checked, the resource that is part of a layer will also be deleted from its corresponding store if the layer is deleted.

* *Overwrite layers when uploading group*. When uploading a group, if this option is not enabled, the Explorer will try to reuse layers that already exist in the catalog. If a layer with the same name already exist, it will be used for the group, and the corresponding QGIS layer will not be uploaded. Check it if you want all layers to be imported, overwriting layers with the same name that might exist in the catalog.


.. _styling_limitations:

Styling limitations
-------------------

The OpenGeo explorer allows to edit the style of a GeoServer layer directly from the QGIS interface. It can convert a style defined in QGIS into a style to be uploaded to a GeoServer catalog, and use GeoServer styles for QGIS layers. This bidirectional conversion is, however, limited. This is mainly caused due to the different versions of the SLD standard that are supported by QGIS and GeoServer, and also to some limitations in both GeoServer and QGIS. SLD is used as the common format used by the OpenGeo Explorer for describing styles in both QGIS and GeoServer layer, but some incompatibilities exist. To increase compatibility between them, specific routines have been added to the OpenGeo explorer. However, in some cases, a style defined in QGIS might not be compatible with the elements supported by GeoServer, and publishing a layer will be done with a modified style, or even using a default one instead if that is not possible.

This problem exist even when using the Suite GeoServer, but older versions of GeoServer might show more incompatibilities and not validate a large part of the SLD produced by the OpenGeo Explorer.

As a rule of thumb, basic styling for vector layers should work without problems in both direction, but more complex symbology might be partially or even completely incompatible, leading to differences between in, for example, the style that you define in QGIS and the style that the GeoServer layer will have. Raster layers have a more limited support

The following is a list of known limitations in SLD handling:

* Raster layers

  * Raster styling is supported only from QGIS to GeoServer. That means that a raster style can be created using the QGIS UI and uploaded to GeoServer, but a raster style from a GeoServer cannot be used for a QGIS layer. When a GeoServer layer is added to the current QGIS project using the OpenGeo Explorer, it will use its symbology only if it is a vector layer, but will ignore it in the case of a raster layer and the default QGIS style will be used.

  * Only *Singleband Gray* and *Singleband pseudocolor* renderers are supported. In this last case, the *Exact* color interpolation is not supported, but *Linear* and *Discrete* modes are supported.

* Vector layers

  * When converting from a GeoServer style to a QGIS style, the style is always defined as a *Rule-based* style. That means that, even if the style is created using another type, such as *Graduated*, when it is uploaded to a GeoServer catalog and then edited again from QGIS, it will not appear as a *Graduated* style. This is due to how QGIS handles SLD styles, always interpreting them as symbology of type *Rule-based*
  * Basic labeling is supported, but not all labeling will be exported from QGIS to SLD and uploaded to GeoServer. In particular, advanced data-dependent labelling is not supported.

.. _pkilimitations:

Limitations when using PKI authentication
------------------------------------------ 

The following operations are not available when connecting to a GeoServer that uses PKI auth:

* GeoNode functionality: GeoNode has a different security mechanism and it is not supported. If a GeoNode URL is entered, it will be ignored when creating the catalog connection.
