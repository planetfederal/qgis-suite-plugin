"""
Dialog to create a user-defined name for a GeoServer component, with optional
validation.
"""

from PyQt4 import QtGui, QtCore

APP = None
if __name__ == '__main__':
    import sys
    # instantiate QApplication before importing QtGui subclasses
    APP = QtGui.QApplication(sys.argv)

from opengeo.gui.gsnameutils import GSNameWidget


# noinspection PyAttributeOutsideInit, PyPep8Naming
class GSNameDialog(QtGui.QDialog):

    def __init__(self, boxtitle='', boxmsg='', name='', namemsg='',
                 nameregex='', nameregexmsg='', names=None,
                 unique=False, maxlength=0, parent=None):
        super(GSNameDialog, self).__init__(parent)
        self.boxtitle = boxtitle
        self.boxmsg = boxmsg
        self.nameBox = GSNameWidget(
            name=name,
            namemsg=namemsg,
            nameregex=nameregex,
            nameregexmsg=nameregexmsg,
            names=names,
            unique=unique,
            maxlength=maxlength
        )
        self.initGui()

    def initGui(self):
        self.setWindowTitle('Define name')
        vertlayout = QtGui.QVBoxLayout()

        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle(self.boxtitle)
        self.groupBox.setLayout(vertlayout)

        if self.boxmsg:
            self.groupBoxMsg = QtGui.QLabel(self.boxmsg)
            self.groupBoxMsg.setWordWrap(True)
            self.groupBox.layout().addWidget(self.groupBoxMsg)

        self.groupBox.layout().addWidget(self.nameBox)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.okButton = self.buttonBox.button(QtGui.QDialogButtonBox.Ok)
        self.cancelButton = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        self.nameBox.nameValidityChanged.connect(self.okButton.setEnabled)
        self.nameBox.overwritingChanged.connect(self.updateButtons)

        # noinspection PyUnresolvedReferences
        self.buttonBox.accepted.connect(self.accept)
        # noinspection PyUnresolvedReferences
        self.buttonBox.rejected.connect(self.reject)

        self.setMinimumWidth(240)

        # respond to intial validation
        self.okButton.setEnabled(self.nameBox.isValid())
        self.updateButtons(self.nameBox.overwritingName())

    def definedName(self):
        return self.nameBox.definedName()

    def overwritingName(self):
        return self.nameBox.overwritingName()

    @QtCore.pyqtSlot(bool)
    def updateButtons(self, overwriting):
        txt = "Overwrite" if overwriting else "OK"
        self.okButton.setText(txt)
        self.okButton.setDefault(not overwriting)
        self.cancelButton.setDefault(overwriting)


if __name__ == '__main__':
    from opengeo.gui.gsnameutils import \
        xmlNameFixUp, xmlNameRegex, xmlNameRegexMsg
    gdlg = GSNameDialog(
        boxtitle='GeoServer data store name',
        boxmsg='My groupbox message',
        namemsg='Sample is generated from PostgreSQL connection name.',
        # name=xmlNameFixUp('My PG connection'),
        name='name_one',
        nameregex=xmlNameRegex(),
        nameregexmsg=xmlNameRegexMsg(),
        names=['name_one', 'name_two'],
        unique=False,
        maxlength=10)
    gdlg.exec_()
    print gdlg.definedName()
    print gdlg.overwritingName()
    # and with no kwargs
    gdlg = GSNameDialog()
    gdlg.exec_()
    print gdlg.definedName()
    print gdlg.overwritingName()
    # gdlg.show()
    # gdlg.raise_()
    # gdlg.activateWindow()
    # sys.exit(APP.exec_())
