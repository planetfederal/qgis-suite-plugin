from opengeo.core import util
from PyQt4 import QtGui, QtCore

class TreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, element, icon = None, text = None): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.element = element    
        self.setData(0, QtCore.Qt.UserRole, element)            
        text = text if text is not None else util.name(element)
        self.setText(0, text)      
        if icon is not None:
            self.setIcon(0, icon)   
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)               
            
    def refreshContent(self):
        self.takeChildren()
        self.populate()    
    
    def descriptionWidget(self):
        widget = QtGui.QTextEdit(None)
        widget.setText("No description available for this element")   
        return widget 
    
    def contextMenuActions(self, explorer):
        return []   
    
    def multipleSelectionContextMenuActions(self, explorer, selected):
        return []
    
    def acceptDroppedItem(self, explorer, item):
        return []