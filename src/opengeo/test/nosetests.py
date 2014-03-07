'''
Tests for the OpenGeo Explorer.
This suite requires a GeoServer catalog running on localhost:8080 with default credentials.
It also requires a running PostGIS on localhost:54321 with default credentials (postgres/postgres)
and a database named "opengeo"

To run, open the python console in qgis and run the following:

  from opengeo.test import run_nose
  run_nose()

A test project will be added after the first step.

Test results will be stored in [tmpdir]/qgis-test-output

If you want to see the test output once the test suite has been run, set the 'open' argument to True
when calling the test runner

    run_nose(open=True)
    
After running, two browser windows should open with the test + coverage results.
'''

import nose
from nose_html import HTML
from opengeo import config
import os
from os.path import (
    abspath, dirname, join
)
import sys
import tempfile
import webbrowser


# load the project required for testing
projectFile = join(dirname(__file__), "data", "test.qgs")
config.iface.addProject(projectFile)

# nose configuration
output_dir = join(tempfile.gettempdir(), 'qgis-test-output')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
coverage_dir = join(output_dir, 'coverage')
xunit_file = join(output_dir, 'xunit-report.xml')
html_file = join(output_dir, 'tests-report.html')
base_nose_args = ['nose',
    '--nocapture', # prevent from stdout hijacking
    '--with-coverage',
        '--cover-html', '--cover-html-dir=%s' % coverage_dir,
        '--cover-package=opengeo',
    '--with-xunit',
        '--xunit-file=%s' % xunit_file,
    '--with-html',
        '--html-file=%s' % html_file,
]

# add a pattern to discover our tests
base_nose_args.append('-i.*tests')


def run_nose(module='opengeo.test', open=False):
    '''run tests via nose
    module - defaults to 'opengeo.test' but provide a specific module or test
             like 'package.module' or 'package.module:class' or
             'package.module:class.test'
    open - open results in browser
    '''

    print 'writing test output to %s' % output_dir

    # and only those in this package
    nose_args = base_nose_args + [module]

    # if anything goes bad, nose tries to call usage so hack this in place
    sys.argv = ['nose']
    try:
        # ugly - coverage will plop down it's file in cwd potentially causing
        # failures if not writable
        cwd = os.getcwd()
        os.chdir(output_dir)
        nose.run(exit=False, argv=nose_args, addplugins=[HTML()])
    except SystemExit:
        # keep invalid options from killing everything
        # optparse calls sys.exit
        pass
    finally:
        sys.argv = None
        # change back to original directory
        os.chdir(cwd)

    if open:
        webbrowser.open(join(coverage_dir, 'index.html'))
        webbrowser.open(html_file)
