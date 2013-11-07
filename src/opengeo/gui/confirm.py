'''
Routines to ask for confirmation when performing certain operations 
'''
from PyQt4 import QtGui, QtCore

def _confirmationBox(title, msg):
    QtGui.QApplication.restoreOverrideCursor()
    ret = QtGui.QMessageBox.warning(None, title, msg,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    return ret == QtGui.QMessageBox.Yes         
    
    
def publishLayer (catalog, layer, workspace=None, overwrite=True, name=None):
    gslayer = catalog.catalog.get_layer(layer.name())
    if gslayer is None or _confirmationBox("Confirm overwrite", 
            "A layer named '%s' already exists in the catalog\nDo you want to overwrite it?" % layer.name()):
        catalog.publishLayer(layer, workspace, overwrite, name)
        
def confirmDelete():
    askConfirmation = bool(QtCore.QSettings().value("/OpenGeo/Settings/General/ConfirmDelete", True, bool))
    if not askConfirmation:
        return True
    msg = "You confirm that you want to delete the selected elements?"
    reply = QtGui.QMessageBox.question(None, "Delete confirmation",
                                               msg, QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    return reply != QtGui.QMessageBox.No
                        
