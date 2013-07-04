# -*- coding: utf-8 -*-

import os, sys
import inspect
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from qgis.core import *
from opengeo import config

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class OpenGeoPlugin:

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
        
    def unload(self):
        pass

    def initGui(self):
        pass
        #=======================================================================
        # publishLayerAction = QAction( u"Publish Layer", self.iface.legendInterface())
        # publishLayerAction.triggered.connect(self.publishLayer)
        # self.iface.legendInterface().addLegendLayerAction(publishLayerAction, u"My Plugin Menu", u"id1", QgsMapLayer.VectorLayer, True )
        #=======================================================================
