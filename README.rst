suite-qgis-plugin
=================

A plugin to configure and OpenGeo suite (mostly its GeoServer component) from QGIS

Installation
--------------

This plugin needs QGIS 2.0 to run (v2.0 hasn't been officialy released yet, so you should use the current development version, also known as QGIS-dev or QGIS-master)

To install the plugin, follow these steps:

- Clone this repository in your system. 
- Locate the QGIS plugins folder. In Windows, it should be something like ``C:\Users\<your_user>\.qgis2\python\plugins``. In Linux/Mac, it should be in ``~/.qgis2/python/plugins``
- Copy the ``opengeo`` folder (can be found under ``src``) into your plugins folder. You should end up having a ``.qgis2\python\plugins\opengeo`` folder with the code of the plugin and the required subfolders. The ``plugin.py`` file should be on that folder.
- Start QGIS and activate the plugin in the plugin manager.
- You should have an *OpenGeo* menu already available in the menu bar.


Usage
------

The plugin functionality is accessed through the GeoServer Eplorer, which is documented `here <./blob/master/doc/gui.rst>`_