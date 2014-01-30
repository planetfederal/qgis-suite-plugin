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

If you want to run the tests, you will also need:

- nose
- nose_html
- coverage

Automated installation using paver
-----------------------------------

A paver script is included in the repository source code.

You will need the python tool :program:`paver` installed to run it.

To do all the setup, run the ``setup`` task

::

	$ paver setup

That will take care of downloading and installing all dependencies in a folder name ``ext-libs`` in the plugin code folder.

To install the plugin into your QGIS, the content of the code folder (named ``opengeo``)  has to be copied to the QGIS plugins folder. There is a task named ``install`` that will take care of that.

::

	$ paver install

If your operating system supports symbolic links (Linux, OSX, Solaris), the ``install`` target must only be run once. On Windows, ``install`` should be run after every code change or repository update.

Manual installation
--------------------

In case you have problems using the setup script, you can install dependencies manually by installing them in your Python installation using a tools such as ``pip`` or ``easy_install``. Of course, you will need to install them in the Python installation used by QGIS. If you prefer, you can add the code of those libraries to the plugin code, as the paver script does. All libraries should be in a folder named ``ext-libs`` under the ``opengeo`` folder, resulting in a tree like the following one.

::

	opengeo
	├───ext-libs
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

You should clone/download the code of those dependencies, and then copy or symlink the corresponding folders in the ``ext-libs`` folder.

The plugin adds the ``ext-libs`` folder to the Python path automatically when it is loaded by QGIS. Make sure you add it as well in case you are setting up your system this way instead of installing the libraries manually.


