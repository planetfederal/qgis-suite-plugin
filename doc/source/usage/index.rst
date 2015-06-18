.. _usage:

Usage
-----

OpenGeo Explorer is launched from the :guilabel:`OpenGeo` menu:

.. todo:: Link to menu image

The brings up a panel in QGIS. The main element of this panel is the tree. It has the following main branches, each of which deals with a different component.

* GeoServer Catalogs
* PostGIS Connections
* QGIS Project

.. note:: A :guilabel:`GeoWebCache` branch is found under :guilabel:`Geoserver Catalogs`, since GeoWebCache is integrated into GeoServer.

The :guilabel:`GeoServer Catalogs` branch contains a list of the catalogs of all connected GeoServer instances. Once instances are added to this branch, you can interact with this GeoServer form within this panel, including publishing layers and styles.

The :guilabel:`PostGIS Databases` branch contains a list of all connected PostGIS databases. Its functionality resembles that of the DB Manager in QGIS. Once databases are added here, you can interact with them from within this panel, including viewing and adding tables.

The :guilabel:`QGIS Project` branch contains the elements of the current QGIS project.

.. note:: The elements in the QGIS Project branch are presented with a structure that more resembles the elements in GeoServer, making publishing easier.

The lower part of the panel contains an information window showing the description of the currently selected item, and also contains links to actions that are related to the current element. 

.. figure:: img/description_panel.png

.. note:: When the panel is undocked, the information window appears to the right of the tree.

   .. figure:: img/undocked.png

The information window can also show tables where parameters can be edited. The one shown below corresponds to the :guilabel:`Settings` element of a GeoServer catalog.

.. figure:: img/description_table.png

Accessing the functionality of OpenGeo Explorer is done through context menus (right-clicking), or through the buttons in the toolbar above the tree. These buttons change depending on what is selected, and are identical to the items found in the context menu.

To see command functionality used in OpenGeo Explorer, please see the :ref:`tutorial` page. For a comprehensive reference of all possible options, please see the :ref:`actions` section.


