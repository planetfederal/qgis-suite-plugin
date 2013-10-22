.. _developers:

Setting up the OpenGeo Explorer code for development
=====================================================

This section explains how to prepare a development environment for those wanting to work with the Explorer code and contribute to the project.

First, clone the OpenGeo Explorer repository

::

	$ git clone https://github.com/boundlessgeo/suite-qgis-plugin.git

The repository contains all the code of the plugin, but not the code of the libraries it depends on. Since the QGIS plugin manager does not allow to install dependencies when installing a plugin, the Explorer plugin itself contains the code of those libraries, but in this case you should install them manually.

These are the libraries that the OpenGeo Explorer requires.

- httplib2 (http://code.google.com/p/httplib2/)
- raven (http://github.com/getsentry/raven-python)
- requests (http://www.python-requests.org/en/latest/)

You can install those libraries in your Python installation (and, of course, in the Python installation used by QGIS) using a tool such as ``pip`` or ``easy_install``. Also, you can add the code of those libraries to the plugin code. All libraries should be in a folder named ``ext_libs`` under the ``opengeo`` folder, resulting in a tree like the following one.

::

	opengeo
	├───ext_libs
	│   ├───httplib2
	│   ├───raven
	│   │   ├───conf
	│   │   ├───contrib
	│   │   │   ├───bottle
	│   │   │   ├───celery
	│   │   │   ├───django
	│   │   │   │   ├───celery
	│   │   │   │   ├───management
	│   │   │   │   │   └───commands
	│   │   │   │   ├───middleware
	│   │   │   │   ├───raven_compat
	│   │   │   │   │   ├───management
	│   │   │   │   │   │   └───commands
	│   │   │   │   │   ├───middleware
	│   │   │   │   │   └───templatetags
	│   │   │   │   └───templatetags
	│   │   │   ├───flask
	│   │   │   ├───pylons
	│   │   │   ├───tornado
	│   │   │   ├───transports
	│   │   │   │   └───zeromq
	│   │   │   ├───webpy
	│   │   │   ├───zerorpc
	│   │   │   └───zope
	│   │   ├───handlers
	│   │   ├───scripts
	│   │   ├───transport
	│   │   └───utils
	│   │       └───serializer
	│   └───requests
	│       └───packages
	│           ├───charade
	│           └───urllib3
	│               ├───contrib
	│               └───packages
	│                   └───ssl_match_hostname
	├───geoserver
	├───gui
	│   └───dialogs
	├───images
	├───postgis
	├───qgis
	└───resources

This is how the code should be structured once copied to the QGIS plugins folder, in case you haven't added the libraries in the Python installation used by QGIS. As explained, this is due to the limitations of the QGIS plugin installer, so the plugin package contains the required libraries in it instead of assuming they are installed and available.

You should clone/dowload the code of those dependencies, and then copy or symlink the corresponding folders in the ``ext_libs`` folder.

The plugin adds the ``ext_libs`` folder to the Python path automatically when it is loaded by QGIS. Make sure you add it as well in case you are setting up your system this way instead of installing the libraries manually.

A python script to package and copy the code to your QGIS plugins folder is available in the ``install.py`` script. If you have a standard QGIS installation, you should be able to execute without modifications, and have the Explorer plugin added to the list of available QGIS plugins.

