.. _install:

Installation
============

This section will describe how to install the OpenGeo Suite for QGIS plugin.

.. warning:: The OpenGeo Suite for QGIS plugin is not bundled with `OpenGeo Suite <http://boundlessgeo.com/solutions/opengeo-suite/>`_.

The OpenGeo Suite plugin requires QGIS version 2.0 or higher to run. It is installed using the Plugin Manager.

#. Navigate to :menuselection:`Plugins --> Manage and Install Plugins`.

#. Click :guilabel:`Settings`

#. As the plugin is still in development, it is tagged as "experimental." Check the box that says :guilabel:`Show also experimental plugins`.

#. In the list of :guilabel:`Plugin repositories`, click :guilabel:`Add`.

#. Add the following repository to the list of plugin repositories:

   * **Name**: Boundless plugin repository
   * **URL**: http://qgis.boundlessgeo.com/plugins.xml

   .. figure:: img/actions/plugin_repo.png

      Adding a new plugin repository

#. Click :guilabel:`OK`.

#. Now the OpenGeo Suite plugin should be available and ready to be installed.

   .. figure:: img/actions/plugin_repo_added.png

      New plugin repository added successfully

 Click :guilabel:`Get More` to see a list of new plugins that can be installed.

#. You should see one titled :guilabel:`OpenGeo Explorer`. Click :guilabel:`Install plugin`.

   .. note:: If you don't see the plugin, ensure that you checked :guilabel:`Show also experimental plugins`.

   .. figure:: img/actions/plugin_install.png

      OpenGeo in the list of plugins

#. The plugin will be downloaded and installed. To verify that installation was successful, you should see a new menu in the menu bar called :guilabel:`OpenGeo`.

   .. figure:: img/actions/plugin_menu.png

      OpenGeo menu