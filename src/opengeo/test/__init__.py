
import unittest
import catalogtests
from opengeo import config
import os
import guitests
import dragdroptests

def suite():
    suite = unittest.TestSuite()
    suite.addTests(catalogtests.suite())
    suite.addTests(guitests.suite())
    suite.addTests(dragdroptests.suite())        
    return suite


def runtests(outputFile = None):    
    projectFile = os.path.join(os.path.dirname(__file__), "data", "test.qgs")
    config.iface.addProject(projectFile)
    if file is None:
        result = unittest.TestResult()
        suite().run(result)
        return result
    else:
        with open(outputFile, "w") as f:   
            unittest.TextTestRunner(f).run(suite())    
    
    