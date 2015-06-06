.. _install:

Installation
============

This section will describe how to install the OpenGeo Explorer plugin.

Installing using the Plugin Manager (recommended)
-------------------------------------------------

The OpenGeo Explorer plugin requires **QGIS version 2.8 or higher** to run. It is recommended to be installed using the QGIS Plugin Manager.

#. In QGIS, navigate to :menuselection:`Plugins --> Manage and Install Plugins`.

#. Click :guilabel:`Settings`

#. Scroll down to the bottom and click :guilabel:`Add`.

#. Add the following repository to the list of plugin repositories:

   * **Name**: Boundless plugin repository
   * **URL**: http://qgis.boundlessgeo.com/plugins.xml

   .. figure:: img/actions/plugin_repo.png

      Adding a new plugin repository

#. Click :guilabel:`OK`.

   .. figure:: img/actions/plugin_repo_added.png

      New plugin repository added successfully

#. With the Boundless repository added, the OpenGeo Explorer plugin will not be available to be installed. Click :guilabel:`Not Installed` to see a list of all plugins.

#. You should see one titled :guilabel:`OpenGeo Explorer`. Select it and click :guilabel:`Install plugin`.

   .. figure:: img/actions/plugin_install.png

      OpenGeo Explorer in the list of plugins

#. The plugin will be installed. To verify that installation was successful, you should see a new menu in the QGIS menu bar called :guilabel:`OpenGeo`.

   .. figure:: img/actions/plugin_menu.png

      OpenGeo menu

Installing from a ZIP file
--------------------------

If you have a copy of the plugin code in a ZIP file, you can install it by unzipping it into the QGIS plugins folder.

* For Windows, it will be similar to :file:`C:\\Users\\<your_user>\\.qgis2\\python\\plugins`.
* For Linux/Mac, it will be :file:`~/.qgis2/python/plugins`.

Copy the ``opengeo`` folder in the ZIP file into your ``plugins`` folder. The ``plugin.py`` file should be in that folder. Form there you can enable the plugin as above.

Getting the development version
-------------------------------

The plugin repository (http://qgis.boundlessgeo.com) is updated frequently. However, to be sure that you are using the latest development version, follow the steps described in the :ref:`developers <developers>` section.
