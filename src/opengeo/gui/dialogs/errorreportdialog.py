from PyQt4 import QtGui

class ErrorReportDialog(QtGui.QDialog):

    def __init__(self, parent = None):
        super(ErrorReportDialog, self).__init__(parent)
        self.message = None
        self.initGui()

    def initGui(self):
        self.setWindowTitle('Error report')
        verticalLayout = QtGui.QVBoxLayout()

        messageLabel = QtGui.QLabel('Description (describe the operation you were trying to run, which caused this error)')
        verticalLayout.addWidget(messageLabel)
        self.messageText = QtGui.QTextEdit()
        verticalLayout.addWidget(self.messageText)

        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("Error description")
        self.groupBox.setLayout(verticalLayout)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        verticalLayout.addWidget(self.buttonBox)

        self.setLayout(verticalLayout)

        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)

        self.resize(400,200)


    def okPressed(self):
        self.message = unicode(self.messageText.toPlainText())
        self.close()

    def cancelPressed(self):
        self.message = None
        self.close()