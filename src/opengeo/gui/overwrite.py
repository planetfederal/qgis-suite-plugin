'''
Routines to publish to a catalog in a safe mode, asking for overwrite confirmation 
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
    if gslayer is not None and _confirmationBox("Confirm overwrite", 
            "A layer named '%s' already exists in the catalog\nDo you want to overwrite it?" % layer.name()):
        catalog.publishLayer(layer, workspace, overwrite, name)
