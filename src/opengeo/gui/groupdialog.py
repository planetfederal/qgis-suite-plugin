from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from opengeo.core.layergroup import UnsavedLayerGroup

class LayerGroupDialog(QtGui.QDialog):
    def __init__(self, catalog, previousgroup = None):
        self.previousgroup = previousgroup
        self.catalog = catalog        
        QtGui.QDialog.__init__(self)
        self.layers = catalog.get_layers()
        self.layernames = [layer.name for layer in self.layers]
        self.styles = [style.name for style in catalog.get_styles()]
        self.setModal(True)
        self.setupUi()
        self.group = None

    def setupUi(self):                
        self.resize(600, 350)
        self.setWindowTitle("Group definition")
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setMargin(0)        
        self.nameLabel = QtGui.QLabel("Group name")        
        self.nameBox = QtGui.QLineEdit()
        if self.previousgroup:
            self.nameBox.setText(self.previousgroup.name)
        else:
            self.nameBox.setText("Group")
        self.horizontalLayout.addWidget(self.nameLabel)
        self.horizontalLayout.addWidget(self.nameBox)
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0,300)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(["Layer", "Style"])
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.selectAllButton = QtGui.QPushButton()
        self.selectAllButton.setText("(de)Select all")
        self.setTableContent()
        self.buttonBox.addButton(self.selectAllButton, QtGui.QDialogButtonBox.ActionRole)
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        QtCore.QObject.connect(self.selectAllButton, QtCore.SIGNAL("clicked()"), self.selectAll)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setTableContent(self):
        self.table.setRowCount(len(self.layernames))
        previouslayers = self.previousgroup.layers if self.previousgroup is not None else []
        previousstyles = self.previousgroup.styles if self.previousgroup is not None else []
        i = 0
        for layer, style in zip(previouslayers, previousstyles):
            item = QtGui.QCheckBox()
            item.setText(layer)
            item.setChecked(True)
            self.table.setCellWidget(i,0, item)
            item = QtGui.QComboBox()
            item.addItems(self.styles)
            try:
                idx = self.styles.index(style)
                item.setCurrentIndex(idx)
            except ValueError:
                pass
            self.table.setCellWidget(i,1, item)
            i += 1        
        for layer in self.layers:
            if layer.name not in previouslayers:
                item = QtGui.QCheckBox()
                item.setText(layer.name)
                self.table.setCellWidget(i,0, item)
                item = QtGui.QComboBox()
                item.addItems(self.styles)
                try:
                    idx = self.styles.index(layer.default_style.name)
                    item.setCurrentIndex(idx)
                except ValueError:
                    pass 
                self.table.setCellWidget(i,1, item)
                i += 1

    def okPressed(self):
        self.name = self.nameBox.text()
        if self.name.strip() == "":
            return
            #TODO show alert
        layers = []
        styles = []
        for i in range(len(self.layernames)):
            widget = self.table.cellWidget(i, 0)
            if widget.isChecked():
                layers.append(widget.text())
                styleWidget = self.table.cellWidget(i, 1)
                styles.append(styleWidget.currentText())
        if len(self.layernames) == 0:
            return
            #TODO show alert
        if self.previousgroup is not None:
            self.group = self.previousgroup
            self.group.dirty.update(layers = layers, styles = styles)
        else:
            #TODO compute bounds
            bbox = None
            self.group =  UnsavedLayerGroup(self.catalog, self.name, layers, styles, bbox)
        self.close()

    def cancelPressed(self):
        self.group = None
        self.close()

    def selectAll(self):
        checked = False
        for i in range(len(self.layernames)):
            widget = self.table.cellWidget(i, 0)
            if not widget.isChecked():
                checked = True
                break
        for i in range(len(self.layernames)):
            widget = self.table.cellWidget(i, 0)
            widget.setChecked(checked)
            
