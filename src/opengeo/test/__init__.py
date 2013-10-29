
import unittest
import catalogtests
from opengeo import config
import os
import guitests
import dragdroptests
from opengeo.test import deletetests


'''
Tests for the OpenGeo Explorer.
This suite requires a GeoServer catalog running on localhost:8080 with default credentials.
It also requires a running PostGIS on localhost:54321 with default credentials (postgres/postgres) 
and a database named "opengeo"    
'''
    
def suite():
    suite = unittest.TestSuite()
    suite.addTests(catalogtests.suite())
    suite.addTests(guitests.suite())
    suite.addTests(dragdroptests.suite())
    suite.addTests(deletetests.suite())        
    return suite


def runtests(outputFile = None):    
    projectFile = os.path.join(os.path.dirname(__file__), "data", "test.qgs")
    config.iface.addProject(projectFile)
    if outputFile is None:
        result = unittest.TestResult()
        suite().run(result)
        return result
    else:
        with open(outputFile, "w") as f:   
            unittest.TextTestRunner(f).run(suite())    
    
    