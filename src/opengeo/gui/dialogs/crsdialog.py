from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

class CrsSelectionDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.authid = None
        layout = QVBoxLayout()
        self.selector = QgsProjectionSelector(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        layout.addWidget(self.selector)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, SIGNAL("rejected()"), self.cancelPressed)

    def okPressed(self):
        self.authid = self.selector.selectedAuthId()
        self.close()

    def cancelPressed(self):
        self.authid = None
        self.close()
