from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from layerdialog import PublishLayersDialog
from geoserver.layergroup import UnsavedLayerGroup
from opengeo.gui.gsnameutils import GSNameWidget, \
    xmlNameFixUp, xmlNameRegexMsg, xmlNameRegex

class LayerGroupDialog(QtGui.QDialog):
    def __init__(self, catalog, previousgroup = None):
        self.previousgroup = previousgroup
        self.catalog = catalog        
        QtGui.QDialog.__init__(self)
        self.groups = catalog.get_layergroups()
        self.groupnames = [group.name for group in self.groups]
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
        self.verticalLayout.setMargin(6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        # self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setMargin(0)
        self.nameLabel = QtGui.QLabel("Group name")
        self.nameLabel.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred))
        defaultname = "Group"
        if self.previousgroup:
            defaultname = self.previousgroup.name
        self.nameBox = GSNameWidget(
            namemsg='',
            name=defaultname,
            nameregex=xmlNameRegex(),
            nameregexmsg=xmlNameRegexMsg(),
            names=self.groupnames,
            unique=False if self.previousgroup else True)
        if self.previousgroup:
            self.nameBox.setEnabled(False)
        self.nameBox.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred))

        self.horizontalLayout.addWidget(self.nameLabel)
        self.horizontalLayout.addWidget(self.nameBox)
        self.verticalLayout.addLayout(self.horizontalLayout)        
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
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
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.selectAllButton.clicked.connect(self.selectAll)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.nameBox.nameValidityChanged.connect(self.okButton.setEnabled)
        self.nameBox.overwritingChanged.connect(self.updateButtons)
        self.okButton.setEnabled(self.nameBox.isValid())
        self.updateButtons(self.nameBox.overwritingName())

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
                except:                    
                    pass 
                self.table.setCellWidget(i,1, item)
                i += 1

    @QtCore.pyqtSlot(bool)
    def updateButtons(self, overwriting):
        txt = "Overwrite" if overwriting else "OK"
        self.okButton.setText(txt)
        self.okButton.setDefault(not overwriting)
        self.cancelButton.setDefault(overwriting)

    def okPressed(self):
        self.name = unicode(self.nameBox.definedName())
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


# noinspection PyPep8Naming
class PublishLayerGroupDialog(QtGui.QDialog):
    def __init__(self, catalog, groupname, layers, workspace=None,
                 overwritegroup=True, overwritelayers=True, parent = None):
        QtGui.QDialog.__init__(self)
        self.catalog = catalog  # GS catalog
        self.groupname = groupname
        self.layers = layers
        self.workspace = workspace
        self.overwritegrp = overwritegroup
        self.overwritelyrs = overwritelayers
        self.groupnames = [grp.name for grp in catalog.get_layergroups()]
        self.definedname = None
        self.topublish = None
        self.setModal(True)
        self.setupUi()

    # noinspection PyAttributeOutsideInit
    def setupUi(self):
        self.resize(600, 350)
        self.setWindowTitle("Publish Group")
        vertlayout = QtGui.QVBoxLayout(self)
        vertlayout.setSpacing(2)
        vertlayout.setMargin(6)
        horizlayout = QtGui.QHBoxLayout(self)
        # horizlayout.setSpacing(30)
        horizlayout.setMargin(0)
        self.nameLabel = QtGui.QLabel("Group name")
        self.nameLabel.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,
                              QtGui.QSizePolicy.Preferred))
        self.nameBox = GSNameWidget(
            name=xmlNameFixUp(self.groupname),
            nameregex=xmlNameRegex(),
            nameregexmsg=xmlNameRegexMsg(),
            names=self.groupnames,
            unique=not self.overwritegrp)
        self.nameBox.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Preferred))
        horizlayout.addWidget(self.nameLabel)
        horizlayout.addWidget(self.nameBox)
        vertlayout.addLayout(horizlayout)

        self.lyrstable = PublishLayersDialog(
            {0: self.catalog}, self.layers,
            workspace=self.workspace, overwrite=self.overwritelyrs)
        self.lyrstable.buttonBox.setVisible(False)
        vertlayout.addWidget(self.lyrstable)

        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        vertlayout.addWidget(self.buttonBox)

        self.setLayout(vertlayout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.nameBox.nameValidityChanged.connect(self.okButton.setEnabled)
        self.nameBox.overwritingChanged.connect(self.updateButtons)
        self.okButton.setEnabled(self.nameBox.isValid())
        self.updateButtons(self.nameBox.overwritingName())

        self.lyrstable.itemValidityChanged.connect(self.okButton.setEnabled)
        self.okButton.setEnabled(self.lyrstable.layerNamesValid())

    @QtCore.pyqtSlot(bool)
    def updateButtons(self, overwriting):
        txt = "Overwrite" if overwriting else "OK"
        self.okButton.setText(txt)
        self.okButton.setDefault(not overwriting)
        self.cancelButton.setDefault(overwriting)

    def okPressed(self):
        self.definedname = self.nameBox.definedName()
        self.topublish = self.lyrstable.layersToPublish()
        self.close()

    def cancelPressed(self):
        self.definedname = None
        self.topublish = None
        self.close()
