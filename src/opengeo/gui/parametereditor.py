from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ParameterEditor(QtGui.QWidget):
    def __init__(self, settings):
        self.settings = settings
        self.parameters = settings.settings()
        QtGui.QWidget.__init__(self)                
        self.setupUi()

    def setupUi(self):                
        layout = QVBoxLayout()        
        self.tree = QtGui.QTreeWidget()
        self.tree.setAlternatingRowColors(True)        
        self.tree.headerItem().setText(0, "Setting")
        self.tree.headerItem().setText(1, "Value")
        self.tree.setColumnWidth(0, 150)
        layout.addWidget(self.tree)
        for section in self.parameters:
            params = self.parameters[section]            
            paramsItem = QtGui.QTreeWidgetItem() 
            paramsItem.setText(0, section)                           
            for name, value in params:
                item = QtGui.QTreeWidgetItem()
                item.setText(0, name)
                item.setText(1, value)
                paramsItem.addChild(item)
            self.tree.addTopLevelItem(paramsItem) 
        self.setLayout(layout)

        
