OpenGeo Explorer QGIS Plugin
**************************

A plugin to configure and manage the OpenGeo Suite from QGIS

Installation
--------------

This plugin needs QGIS 2.0 to run. Previous versions of QGIS will not be able to run the OpenGeo Explorer

The plugin is installed using the plugin manager.

- Add the following repository to the list of plugin repositories:

	.. image:: doc/source/manual/plugin_repo.png

- Now the OpenGeo Suite plugin should be available and ready to be installed. You can look for it in the list of installable plugins in the  plugin manager.
	
	.. image:: doc/source/manual/plugin_install.png

- Click on *Install plugin*. The plugin will be downloaded and installed.

Installing the current development version
-------------------------------------------

The plugin repository is updated frequently- However, it is not guaranteed that it will contain the same code that can be found in this GitHub repository. If you want to be sure that you are using the latest development version, follow the next steps.

- Clone this repository in your system. 
- Locate the QGIS plugins folder. In Windows, it should be something like ``C:\Users\<your_user>\.qgis2\python\plugins``. In Linux/Mac, it should be in ``~/.qgis2/python/plugins``
- Copy the ``opengeo`` folder (can be found under ``src``) into your plugins folder. You should end up having a ``.qgis2\python\plugins\opengeo`` folder with the code of the plugin and the required subfolders. The ``plugin.py`` file should be on that folder.
- Start QGIS and activate the plugin in the plugin manager.
- You should have an *OpenGeo* menu already available in the menu bar.

Usage
------

The plugin functionality is accessed through the GeoServer Explorer, which is documented `here <./doc/source/manual/gui.rst>`_
