.. _caveats:

Caveats and known issues
========================

This page contains important information about the OpenGeo Explorer plugin. If you encounter problems with using the plugin, check here for potential workaround.

GeoServer and PostGIS synchronization
-------------------------------------

Except for the :guilabel:`QGIS Project` item, all remaining items in the OpenGeo Explorer tree are not automatically updated when the element they represent changes. For example, a change in a PostGIS database performed outside of the plugin will not trigger an update in the OpenGeo Explorer tree.

All items have a :guilabel:`Refresh` option. Use it to update the content of a given entry in the tree and keep it synchronized with the corresponding catalog or database.

Version support
---------------

This plugin is targeted at the elements of `OpenGeo Suite <http://boundlessgeo.com/solutions/opengeo-suite/>`_, and it is tested with the most recent release. However, you can use most of the functionality if you are using individual installations of elements such as GeoServer and PostGIS.

.. todo:: Add specific version limitations

To check the version of your catalog, just select the catalog in the tree and look at the description tab. 

.. figure:: ../usage/img/about.png

If you do not see information like that, it is likely that your catalog uses a GeoServer version that doesn't support that operation. In this case, it will not support the other operations that cause problems, so you will probably find some issues when working with the catalog through the plugin.

When connecting to a catalog, the explorer tries to check the version. If it cannot detect the version or it cannot confirm it is the target version, it will ask you before adding the catalog.

.. figure:: img/version_warning.png


Known issues
------------

Even if you are using the correct version of GeoServer, some issues still may occur. Below is a list of know limitations and issues than might appear.

CRS
~~~

GeoServer might encounter problems when a custom CRS is used in QGIS. The CRS definition that works correctly when rendering the layer in QGIS might not work when importing the layer into GeoServer. Usually this results in a layer that is published but doesn't have a CRS set and is not enabled. You can correct that manually, selecting the layer in the Explorer tree and modifying its CRS.

Notice that layers are imported using the SRS defined in the original data source (i.e., the ``prj`` file if using a shapefile). Setting a different CRS using the :guilabel:`Set Layer CRS` option in the QGIS TOC will not have any effect when importing the layer into GeoServer, unless you save the layer with that CRS and the CRS definition is stored along with the layer data.

Layer names
~~~~~~~~~~~

OpenGeo Explorer uses the GeoServer REST API to retrieve the list of layers in a catalog. The REST API describes layers without workspace, that meaning that if you have two layers with the same name and in different workspaces (for instance, ``ws1:mylayer`` and ``ws2:mylayer``), they will be shown as just one (``mylayer`` in this case).

When this happens, the situation is ambiguous and OpenGeo Explorer cannot differentiate between layers with the same name but belonging to different workspaces. The layer, as described by the REST API, is added to the Explorer tree, but it only represents one of the several layers that share the same name. To indicate this, the layer is shown with a warning icon, and a warning message is displayed in the layer description.

.. figure:: img/duplicated_layer.png

.. _styling_limitations:

Styling limitations
~~~~~~~~~~~~~~~~~~~

OpenGeo Explorer allows to edit the style of a GeoServer layer directly from the QGIS interface. It can convert a style defined in QGIS into a style to be uploaded to a GeoServer catalog, and use GeoServer styles for QGIS layers. This bidirectional conversion is, however, limited. This is mainly caused due to the different versions of the SLD standard that are supported by QGIS and GeoServer, and also to some limitations in both GeoServer and QGIS. SLD is used as the common format used by the OpenGeo Explorer for describing styles in both QGIS and GeoServer layer, but some incompatibilities exist. To increase compatibility between them, specific routines have been added to the OpenGeo explorer. However, in some cases, a style defined in QGIS might not be compatible with the elements supported by GeoServer, and publishing a layer will be done with a modified style, or even using a default one instead if that is not possible.

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

PKI authentication limitations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following operations are not available when connecting to a GeoServer that uses PKI auth:

* GeoNode functionality: GeoNode has a different security mechanism and it is not supported. If a GeoNode URL is entered, it will be ignored when creating the catalog connection.


Viewing errors
--------------

When an error is found, a message is shown in the QGIS message bar.

.. figure:: img/error-bar.png

This error might be caused by a wrong usage (for instance, if you are trying to connect to a catalog that does not exist), or by a bug in the plugin. To help us fix this second case, you can report the error by clicking on the :guilabel:`Report error` button that appears in the message bar. This will cause the full error stack trace to be sent automatically, so we can check it and find out the cause of the error. No personal information is sent along with it.

To check the stack trace yourself, click the :guilabel:`View more` button.

If no button is pushed, the message bar will remain visible for 15 seconds. You can close it using the close icon on its right side.

