# -*- coding: utf-8 -*-

"""
***************************************************************************
    ExtentSelectionPanel.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from opengeo.gui.rectangletool import RectangleMapTool
from opengeo import config

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

from qgis.core import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ExtentSelectionPanel(QtGui.QWidget):

    def __init__(self, dialog):
        super(ExtentSelectionPanel, self).__init__(None)
        self.dialog = dialog        
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.text = QtGui.QLineEdit()
        #self.text.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)        
        if hasattr(self.text, 'setPlaceholderText'):
            self.text.setPlaceholderText("[xmin,xmax,ymin,ymax] Leave blank to use full extent")
        self.horizontalLayout.addWidget(self.text)
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setText("Define in canvas")
        self.pushButton.clicked.connect(self.selectOnCanvas)
        self.horizontalLayout.addWidget(self.pushButton)
        self.setLayout(self.horizontalLayout)
        canvas = config.iface.mapCanvas()
        self.prevMapTool = canvas.mapTool()
        self.tool = RectangleMapTool(canvas)
        self.connect(self.tool, SIGNAL("rectangleCreated()"), self.fillCoords)

    def selectOnCanvas(self):
        canvas = config.iface.mapCanvas()
        canvas.setMapTool(self.tool)
        self.dialog.showMinimized()

    def fillCoords(self):
        r = self.tool.rectangle()
        self.setValueFromRect(r)

    def setValueFromRect(self,r):
        s = str(r.xMinimum()) + "," + str(r.xMaximum()) + "," + str(r.yMinimum()) + "," + str(r.yMaximum())
        self.text.setText(s)
        self.tool.reset()
        canvas = config.iface.mapCanvas()
        canvas.setMapTool(self.prevMapTool)
        self.dialog.showNormal()
        self.dialog.raise_()
        self.dialog.activateWindow()


    def getValue(self):
        text = self.text.text().strip()
        if text == "":
            return None
        else:
            return text.split(",")            
