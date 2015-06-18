.. _configuration:

Configuration
=============

Along with the menu entry that starts the Explorer, you will find an entry that opens the configuration window, which looks as shown next.

.. figure:: img/config.png


Use the parameters in this dialog to configure the Explorer to your particular needs. The properties that can be configured are described in detail below.

Tabbed vs single-tab interface
------------------------------

By default, the Explorer shows all categories (GeoServer, PostGIS) in a single panel, as branches in a tree. If you enable the multi-tab user interface, each category is put in a separate tab, and each tab contains a panel with a tree of elements belonging to the corresponding category, as shown in the next figure.

.. figure:: img/multi-tab.png



Functionality can be accessed in the same way as in the default interface, by right clicking on an element or selecting it and using the buttons that will appear in the toolbar on the upper part of the panel. Drag & drop functionality is limited to elements within the same category. 

In case they exist, subcategories (such as layers, workspaces, etc., in the case of a GeoServer catalog) can be switched using the buttons on the lower part of the panel.

When you change the type of UI by changing the corresponding value in the configuration dialog, the Explorer interface is not automatically changed. Restarting QGIS is needed for the change to take effect.

.. _gs_connections:

Keeping a list of previous GeoServer connections
------------------------------------------------

If you enable this option, whenever you connect to a catalog, the information that defines that connections is kept between sessions. Next time that you start QGIS and the OpenGeo Explorer, you will see the catalogs item populated with all the previous connections, as shown in the next picture.

.. figure:: img/gray_catalog.png

Retrieving information from each connection might take a long time and cause QGIS to take too long to start up. For this reason, catalog data is fetch on request and not automatically when starting the OpenGeo Explorer. You should refresh the catalog item to populate it. Unpopulated catalogs are shown with a gray icon.

If the catalog uses basic authentication and username and password are introduced using the basic authentication tab, the password is not stored. You will be prompted to enter it when you reconnect to the catalog. If the *Configurations* tab is used, connection data (wheter password or certificate-based) will be stored in the encrypted QGIS auth database. You will be prompted to enter the master password in case you haven't used the auth database in the current QGIS session.

To know more about how to use authentication configurations in QGIS, see the `Authentication configurations <./auth.html>`_ section

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

