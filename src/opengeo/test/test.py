# -*- coding: utf-8 -*-

import os
import sys
import unittest

from qgistestapp import getQgisTestApp
from opengeo.test import catalogtests, guitests

pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(pardir)


(QGISAPP, CANVAS, IFACE, PARENT) = getQgisTestApp()


def suite():
    suite = unittest.TestSuite()
    suite.addTests(catalogtests.suite())
    suite.addTests(guitests.suite())      
    return suite

def runtests():
    result = unittest.TestResult()
    testsuite = suite()
    testsuite.run(result)
    return result
    

if __name__ == '__main__':        
    unittest.TextTestRunner(verbosity=2).run(suite())
    
