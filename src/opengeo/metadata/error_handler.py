# -*- coding: utf-8 -*-

#******************************************************************************
#
# Metatools
# ---------------------------------------------------------
# Metadata browser/editor
# Copyright (C) 2011 BV (enickulin@bv.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************
from PyQt4.QtXmlPatterns import QAbstractMessageHandler

class ErrorHandler(QAbstractMessageHandler):
  def __init__(self, windowTitle):
    QAbstractMessageHandler.__init__(self)
    self.windowTitle = windowTitle
    self.errorOccured = False

  def resetError(self):
    self.errorOccured = False

  def message(self, msg_type, desc, identifier, loc):
    self.handleMessage(msg_type, desc, identifier, loc)

  def handleMessage(self, msg_type, desc, identifier, loc):
    #QMessageBox.information(None, "Error", desc + " Ident: " + identifier.toString() + " Line: " + QString(str(loc.line())))
    from metatoolsviewer import MetatoolsViewer

    message_type = {0:'Debug', 1:'Warning', 2:'Critical', 3:'Fatal'}

    if msg_type > 1:
        self.errorOccured = True

    desc.replace('<p>', '')
    desc.replace('</p>', '')
    desc.replace("<body>", "<head><style>.XQuery-keyword, .XQuery-type {color: red;} infolabel {color: blue; text-weight: bold; text-size: 14px}</style></head><body>") #add styles 
    desc.replace("<body>", "<infolabel>Problem type: </infolabel>%s <br/><infolabel>Problem line: </infolabel>%s <br/><infolabel>Problem description: </infolabel>" % (message_type[msg_type], loc.line())) #add info

    dlg = MetatoolsViewer()
    dlg.resize(dlg.width(), 200)
    dlg.setHtml(desc)
    dlg.setWindowTitle(self.windowTitle)
    dlg.exec_()
