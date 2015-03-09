'''
Routines to ask for confirmation when performing certain operations 
'''
from PyQt4 import QtGui, QtCore
from opengeo.gui.dialogs.gsnamedialog import getGSLayerName

def _confirmationBox(title, msg):
    QtGui.QApplication.restoreOverrideCursor()
    ret = QtGui.QMessageBox.warning(None, title, msg,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    return ret == QtGui.QMessageBox.Yes


def confirmDelete():
    askConfirmation = bool(QtCore.QSettings().value("/OpenGeo/Settings/General/ConfirmDelete", True, bool))
    if not askConfirmation:
        return True
    msg = "You confirm that you want to delete the selected elements?"
    reply = QtGui.QMessageBox.question(None, "Delete confirmation",
                                               msg, QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    return reply != QtGui.QMessageBox.No
