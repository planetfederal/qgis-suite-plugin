
import unittest
import catalogtests
from opengeo import config
import os
import guitests

def suite():
    suite = unittest.TestSuite()
    suite.addTests(catalogtests.suite())
    suite.addTests(guitests.suite())      
    return suite


def runtests():
    projectFile = os.path.join(os.path.dirname(__file__), "data", "test.qgs")
    config.iface.addProject(projectFile)
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result