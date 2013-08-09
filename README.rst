OpenGeo Suite QGIS Plugin
============================

A plugin to configure the OpenGeo suite from QGIS

Installation
--------------

This plugin needs QGIS 2.0 to run. v2.0 hasn't been officialy released yet, so you should use the current development version, also known as QGIS-dev or QGIS-master. It doesn't have to be the very latest version, but at least it has to contain the SIP API changes (basically, anything more recent than July 2013 should work)

To install the plugin, follow these steps:

- Clone this repository in your system. 
- Locate the QGIS plugins folder. In Windows, it should be something like ``C:\Users\<your_user>\.qgis2\python\plugins``. In Linux/Mac, it should be in ``~/.qgis2/python/plugins``
- Copy the ``opengeo`` folder (can be found under ``src``) into your plugins folder. You should end up having a ``.qgis2\python\plugins\opengeo`` folder with the code of the plugin and the required subfolders. The ``plugin.py`` file should be on that folder.
- Start QGIS and activate the plugin in the plugin manager.
- You should have an *OpenGeo* menu already available in the menu bar.

The plugin can also be installed using the plugin manager.

- Add the following repository to the list of plugin repositories:

	.. image:: doc/img/plugin_repo.png

- Now the OpenGeo Suite plugin should be available and ready to be installed. You can look for it in the list of installable plugins in the  plugin manager.
	
	.. image:: doc/img/plugin_install.png

- Click on *Install plugin*. The plugin will be downloaded and installed.

The plugin repository is updated frequently- However, it is not guaranteed that it will contain the same code that can be found in the GitHub repository. If you want to be sure that you are using the latest development version, use the first installation procedure and install from the GitHub repository.

Usage
------

The plugin functionality is accessed through the OpenGeo Explorer, which is documented `here <https://github.com/opengeo/suite-qgis-plugin/blob/master/doc/gui.rst>`_
